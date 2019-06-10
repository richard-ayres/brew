#!/usr/bin/env python3
import os.path
import logging
import sys

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

    if id:
        recipe = query.get(id)
        result = hal.item(recipe, href='/recipe/{id}'.format(id=id))
        result['profile'] = hal.item(recipe.profile, href='/recipe/{id}/profile'.format(id=id))
        result['grain_bill'] = hal.item(recipe.grain_bill, href='/recipe/{id}/grain_bill'.format(id=id))
        result['hop_schedule'] = hal.item(recipe.hop_schedule, href='/recipe/{id}/hop_schedule'.format(id=id))
        return jsonify(result)

    return jsonify(hal.query(query, href='/recipe'))


@app.route('/recipe', methods=['POST'])
@app.route('/recipe/<id>', methods=['PUT'])
def post_recipe(id=None):

    if id:
        recipe = db_session.query(models.Recipe).get(id)

    else:
        recipe = models.Recipe()
        db_session.add(recipe)

    def load_grain_bill(input):
        """Load the grain bill into the current recipe"""
        gb = models.GrainBill()
        gb.weight = input['weight']
        gb.ebc = input.get('ebc', None)
        gb.extract_max = input.get('extract_max', None)
        gb.fermentability = input.get('fermentability', None)
        gb.fermentable = db_session.query(models.Fermentable).get(input['fermentable'])
        gb.recipe = recipe
        return gb

    def load_hop_schedule(input):
        hop = models.HopSchedule()
        hop.weight = input['weight']
        hop.when = input['when']
        hop.alpha = input.get('alpha', None)
        hop.boil_time = input['boil_time']
        hop.hop = db_session.query(models.Hop).get(input['hop'])
        hop.recipe = recipe
        return hop

    input = request.get_json()
    try:
        recipe.name = input['name']
        if input.get('profile', None):
            if recipe.profile:
                db_session.delete(recipe.profile)
            recipe.profile = models.BrewingProfile(**input['profile'])
            recipe.profile.name = recipe.name

        if input.get('grain_bill', None):
            for gb in recipe.grain_bill:
                db_session.delete(gb)
            db_session.add_all(map(load_grain_bill, input['grain_bill']))

        if input.get('hop_schedule', None):
            for hop in recipe.hop_schedule:
                db_session.delete(hop)
            db_session.add_all(map(load_hop_schedule, input['hop_schedule']))
        user = get_logged_in_user()
        db_session.add(models.UserProfileLink(user=user, profile=recipe.profile))
        db_session.add(models.UserRecipeLink(user=user, recipe=recipe))

        db_session.commit()

    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        return make_response(('Error with recipe', 401))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Item not found', 404))

    result = hal.item(recipe, href='/recipe/{id}'.format(id=id))
    result['profile'] = hal.item(recipe.profile, href='/recipe/{id}/profile'.format(id=id))
    result['grain_bill'] = hal.item(recipe.grain_bill, href='/recipe/{id}/grain_bill'.format(id=id))
    result['hop_schedule'] = hal.item(recipe.hop_schedule, href='/recipe/{id}/hop_schedule'.format(id=id))
    return jsonify(result)


@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    db_session.query(models.UserRecipeLink).filter_by(recipe_id=id).delete()
    db_session.query(models.Recipe).filter_by(id=id).delete()
    db_session.commit()
    return get_recipe()


@app.route('/recipe/<id>/profile', methods=['GET'])
def get_recipe_profile(id):
    recipe = db_session.query(models.Recipe).get(id)
    return jsonify(hal.item(recipe.profile, href='/profile/{id}'.format(id=recipe.profile_id)))


@app.route('/profile/<id>', methods=['GET'])
def get_profile(id):
    return jsonify(hal.item(db_session.query(models.BrewingProfile).get(id), href='/profile/{id}'.format(id=id)))


if __name__ == "__main__":
    app.run()

