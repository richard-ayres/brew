import logging
import sqlalchemy.orm.exc

from flask import session

from models import User
from database import db_session


def get_logged_in_user():
    try:
        user_id = session.get('user_id')
        logging.debug('User ID: {}'.format(user_id))

        if user_id is None:
            logging.error("Session doesn't have user_id")
            return None

        return db_session.query(User).get(user_id)

    except sqlalchemy.orm.exc.NoResultFound:
        logging.error('User not found')
        session.pop('user_id')
        return None

    except Exception as ex:
        logging.error("Exception fetching user: {}".format(ex))
        raise


def user_restrict(query, model):
    """Fix the query by restricting results to those for the logged in user"""
    return query.join(model).filter(model.user == get_logged_in_user())
