from flask import request

from models import User
from database import db_session


def get_logged_in_user():
    user_id = request.args.get('user', None)
    if not user_id:
        return None

    return db_session.query(User).get(user_id)


def user_restrict(query, model):
    """Fix the query by restricting results to those for the logged in user"""
    return query.join(model).filter(model.user == get_logged_in_user())
