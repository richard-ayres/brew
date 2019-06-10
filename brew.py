#!/usr/bin/env python3
import os.path
import logging
import sys

from datetime import datetime

import sqlalchemy.exc
import sqlalchemy.orm.exc

from flask import Flask, jsonify, redirect, request, make_response

import models
import hal

from database import db_session
from user import get_logged_in_user, user_restrict

app = Flask(__name__)


DOCROOT = os.path.dirname(__file__)


@app.route('/')
def home():
    return redirect('/index.html')


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


@app.route('/recipe', methods=['GET'])
@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id=None):
    query = db_session.query(models.Recipe)
    query = user_restrict(query, models.UserRecipeLink)

    if id is None:
        return jsonify(hal.query(query, href='/recipe'))

    recipe = query.filter(models.Recipe.id == id).one_or_none()
    if recipe is None:
        return make_response(('Recipe not found', 404))

    result = hal.item(recipe, href='/recipe/{id}'.format(id=id))
    result['profile'] = hal.item(recipe.profile, href='/recipe/{id}/profile'.format(id=id))
    result['grain_bill'] = hal.item(recipe.grain_bill, href='/recipe/{id}/grain_bill'.format(id=id))
    result['hop_schedule'] = hal.item(recipe.hop_schedule, href='/recipe/{id}/hop_schedule'.format(id=id))
    return jsonify(result)


@app.route('/recipe', methods=['POST'])
@app.route('/recipe/<id>', methods=['PUT'])
def post_recipe(id=None):

    if id:
        recipe = db_session.query(models.Recipe).get(id)

    else:
        recipe = models.Recipe()
        db_session.add(recipe)

    def load_grain_bill(req):
        """Load the grain bill into the current recipe"""
        gb = models.GrainBill()
        gb.weight = req['weight']
        gb.ebc = req.get('ebc', None)
        gb.extract_max = req.get('extract_max', None)
        gb.fermentability = req.get('fermentability', None)
        gb.fermentable = db_session.query(models.Fermentable).get(req['fermentable'])
        gb.recipe = recipe
        return gb

    def load_hop_schedule(req):
        hop = models.HopSchedule()
        hop.weight = req['weight']
        hop.when = req['when']
        hop.alpha = req.get('alpha', None)
        hop.boil_time = req['boil_time']
        hop.hop = db_session.query(models.Hop).get(req['hop'])
        hop.recipe = recipe
        return hop

    req = request.get_json()
    try:
        recipe.name = req['name']
        if req.get('profile', None):
            if recipe.profile:
                db_session.delete(recipe.profile)
            recipe.profile = models.BrewingProfile(**req['profile'])
            recipe.profile.name = recipe.name

        if req.get('grain_bill', None):
            for gb in recipe.grain_bill:
                db_session.delete(gb)
            db_session.add_all(map(load_grain_bill, req['grain_bill']))

        if req.get('hop_schedule', None):
            for hop in recipe.hop_schedule:
                db_session.delete(hop)
            db_session.add_all(map(load_hop_schedule, req['hop_schedule']))

        user = get_logged_in_user()
        db_session.add(models.UserProfileLink(user=user, profile=recipe.profile))
        db_session.add(models.UserRecipeLink(user=user, recipe=recipe))

        db_session.commit()

    except sqlalchemy.exc.IntegrityError as ex:
        db_session.rollback()
        return make_response(('Error with recipe: {}'.format(ex), 401))

    except sqlalchemy.orm.exc.NoResultFound as ex:
        db_session.rollback()
        return make_response(('Item not found: {}'.format(ex), 404))

    result = hal.item(recipe, href='/recipe/{id}'.format(id=recipe.id))
    result['profile'] = hal.item(recipe.profile, href='/recipe/{id}/profile'.format(id=recipe.id))
    result['grain_bill'] = hal.item(recipe.grain_bill, href='/recipe/{id}/grain_bill'.format(id=recipe.id))
    result['hop_schedule'] = hal.item(recipe.hop_schedule, href='/recipe/{id}/hop_schedule'.format(id=recipe.id))

    return jsonify(result)


@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    try:
        recipe = user_restrict(db_session.query(models.Recipe), models.UserRecipeLink).filter(models.Recipe.id==id).one()

        db_session.query(models.UserRecipeLink).filter_by(recipe_id=recipe.id).delete()
        db_session.query(models.Batch).filter_by(recipe_id=recipe.id).update({'recipe_id': None})
        db_session.query(models.HopSchedule).filter_by(recipe_id=recipe.id).delete()
        db_session.query(models.GrainBill).filter_by(recipe_id=recipe.id).delete()
        db_session.query(models.Recipe).filter_by(id=recipe.id).delete()
        db_session.commit()

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Recipe not found', 404))

    return get_recipe()


@app.route('/recipe/<id>/profile', methods=['GET'])
def get_recipe_profile(id):
    try:
        recipe = user_restrict(db_session.query(models.Recipe), models.UserRecipeLink).filter(models.Recipe.id==id).one()
        return jsonify(hal.item(recipe.profile, href='/profile/{id}'.format(id=recipe.profile_id)))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Recipe not found', 404))


@app.route('/recipe/<id>/hop_schedule', methods=['GET'])
def get_recipe_hop_schedule(id):
    try:
        recipe = user_restrict(db_session.query(models.Recipe), models.UserRecipeLink).filter(models.Recipe.id==id).one()
        return jsonify(hal.item(recipe.hop_schedule, href='/recipe/{recipe_id}/hop_schedule'.format(recipe_id=id)))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Recipe not found', 404))


@app.route('/recipe/<id>/grain_bill', methods=['GET'])
def get_recipe_grain_bill(id):
    return make_response(('Not implemented yet', 500))


@app.route('/profile/<id>', methods=['GET'])
def get_profile(id):
    try:
        profile = user_restrict(db_session.query(models.BrewingProfile), models.UserProfileLink).filter(models.BrewingProfile.id==id).one()
        return jsonify(hal.item(profile, href='/profile/{id}'.format(id=id)))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Profile not found', 404))


@app.route('/batch', methods=["POST"])
def new_batch():
    req = request.get_json()

    try:
        query = user_restrict(db_session.query(models.Recipe), models.UserRecipeLink)
        recipe = query.filter(models.Recipe.id == req['recipe_id']).one()

        batch = models.Batch(**req)

        if not batch.profile_id:
            batch.actual_profile = recipe.profile

        if not batch.brew_date:
            batch.brew_date = datetime.now()

        db_session.add(batch)
        db_session.add(models.UserBatchLink(user=get_logged_in_user(), batch=batch))
        db_session.commit()

        return jsonify(hal.item(batch, href='/batch/{id}'.format(id=batch.id)))

    except KeyError:
        db_session.rollback()
        return make_response(('Must supply recipe ID', 401))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Recipe not found', 404))

    except:
        db_session.rollback()
        raise


@app.route('/batch/<id>', methods=["GET"])
def get_batch(id):
    try:
        batch = user_restrict(db_session.query(models.Batch), models.UserBatchLink).filter(models.Batch.id == id).one()
        result = hal.item(batch, href='/batch/{id}'.format(id=id))
        result['profile'] = hal.item(batch.actual_profile, href='/profile/{id}'.format(id=batch.profile_id))
        result['recipe'] = hal.item(batch.recipe, href='/recipe/{id}'.format(id=batch.recipe_id))
        return jsonify(result)

    except sqlalchemy.orm.exc.NoResultFound:
        return make_response(('Batch not found', 404))


@app.route('/batch/<id>', methods=["PUT"])
def put_batch(id):
    req = request.get_json()

    try:
        batch = user_restrict(db_session.query(models.Batch), models.UserBatchLink).filter(models.Batch.id == id).one()

        params = {'brew_date', 'rack_date', 'package_date',
                  'pre_boil_gravity', 'original_gravity', 'final_gravity'}
        for param in params & req.keys():
            setattr(batch, param, req[param])

        db_session.commit()

        return jsonify(hal.item(batch, href='/batch/{id}'.format(id=id)))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Batch not found', 404))

    except:
        db_session.rollback()
        raise


if __name__ == "__main__":
    app.run()

