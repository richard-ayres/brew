from flask import request
from urllib.parse import quote as url_quote


def item(item, root):
    if not isinstance(item, dict):
        if hasattr(item, '__table__'):
            item = {column.name: getattr(item, column.name) for column in item.__table__.columns}
        else:
            item = vars(item)

    item['_links'] = {
        'self': {
            'href': root.rstrip('/') + '/' + url_quote(str(item['id']))
        }
    }

    return item


def _list(items, root, offset=None, limit=None, total=None):
    result = {
        'count': len(items),
        '_embedded': [item(o, root) for o in items],
        '_links': {}
    }

    if (offset is None or limit is None or total is None):
        result['_links']['self'] = {
            'href': root
        }
    else:
        offset = int(offset)
        limit = int(limit)
        total = int(total)
        result['_links']['self'] = {
            'href': "{url}?offset={offset:d}&limit={limit:d}".format(url=root, offset=offset, limit=limit)
        }
        if offset > 0:
            result['_links']['first'] = {
                'href': "{url}?offset={offset:d}&limit={limit:d}".format(url=root, offset=0, limit=limit)
            }
        if offset + limit < total:
            result['_links']['next'] = {
                'href': "{url}?offset={offset:d}&limit={limit:d}".format(url=root, offset=offset+limit, limit=limit)
            }
        if offset + limit < total:
            result['_links']['last'] = {
                'href': "{url}?offset={offset:d}&limit={limit:d}".format(url=root, offset=total-limit, limit=limit)
            }
        if offset - limit > 0:
            result['_links']['prev'] = {
                'href': "{url}?offset={offset:d}&limit={limit:d}".format(url=root, offset=offset-limit, limit=limit)
            }

    return result


def query(query, root):
    total = query.count()

    offset = request.args.get('offset', None)
    limit = request.args.get('limit', None)

    if offset is not None and limit is not None:
        query = query.offset(int(offset)).limit(int(limit))

    return _list(query.all(), root=root, limit=limit, offset=offset, total=total)


