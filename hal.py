from flask import request
from urllib.parse import quote as url_quote


def item(item, **kwargs):
    if isinstance(item, list):
        return _list(item, **kwargs)

    if not isinstance(item, dict):
        if hasattr(item, '__table__'):
            item = {column.name: getattr(item, column.name) for column in item.__table__.columns}
        else:
            item = vars(item)

    item['_links'] = {key: {'href': url_quote(link.format(id=item['id']) if 'id' in item else link)}
                      for key, link in kwargs.items()}

    return item


def _list(items, href, offset=None, limit=None, total=None):
    result = {
        'count': len(items),
        '_embedded': [item(o, href=href + '/{id}') for o in items],
        '_links': {}
    }

    if offset is None or limit is None or total is None:
        result['_links']['self'] = {
            'href': url_quote(href)
        }
    else:
        offset = int(offset)
        limit = int(limit)
        total = int(total)
        result['_links']['self'] = {
            'href': url_quote("{url}?offset={offset:d}&limit={limit:d}".format(url=href, offset=offset, limit=limit))
        }
        if offset > 0:
            result['_links']['first'] = {
                'href': url_quote("{url}?offset={offset:d}&limit={limit:d}".format(url=href, offset=0, limit=limit))
            }
        if offset + limit < total:
            result['_links']['next'] = {
                'href': url_quote("{url}?offset={offset:d}&limit={limit:d}".format(url=href, offset=offset+limit, limit=limit))
            }
        if offset + limit < total:
            result['_links']['last'] = {
                'href': url_quote("{url}?offset={offset:d}&limit={limit:d}".format(url=href, offset=total-limit, limit=limit))
            }
        if offset - limit > 0:
            result['_links']['prev'] = {
                'href': url_quote("{url}?offset={offset:d}&limit={limit:d}".format(url=href, offset=offset-limit, limit=limit))
            }

    return result


def query(query, href):
    total = query.count()

    offset = request.args.get('offset', None)
    limit = request.args.get('limit', None)

    if offset is not None and limit is not None:
        query = query.offset(int(offset)).limit(int(limit))

    return _list(query.all(), href=href, limit=limit, offset=offset, total=total)


