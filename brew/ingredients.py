import sqlalchemy.orm.exc

from flask import jsonify, make_response

import models
import hal

from database import db_session
from user import user_restrict

from .app import app


@app.route('/fermentable', methods=['GET'])
@app.route('/fermentable/<id>', methods=["GET"])
def get_fermentables(id=None):
    query = db_session.query(models.Fermentable)

    if id:
        return jsonify(hal.item(query.get(id), href='/fermentable/{id}'))

    return jsonify(hal.query(query, href='/fermentable'))


@app.route('/hop', methods=['GET'])
@app.route('/hop/<id>', methods=['GET'])
def get_hops(id=None):
    query = db_session.query(models.Hop)

    if id:
        return jsonify(hal.item(query.get(id), href='/hop/{id}'))

    return jsonify(hal.query(query, href='/hop'))


@app.route('/yeast', methods=['GET'])
@app.route('/yeast/<id>', methods=['GET'])
def get_yeast(id=None):
    query = db_session.query(models.Yeast)

    if id:
        return jsonify(hal.item(query.get(id), href='/yeast/{id}'))

    return jsonify(hal.query(query, href='/yeast'))


@app.route('/profile/<id>', methods=['GET'])
def get_profile(id):
    try:
        profile = user_restrict(db_session.query(models.BrewingProfile), models.UserProfileLink).filter(models.BrewingProfile.id==id).one()
        return jsonify(hal.item(profile, href='/profile/{id}'.format(id=id)))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Profile not found', 404))



