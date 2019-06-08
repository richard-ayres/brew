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
        return jsonify(hal.item(query.filter_by(id=id).one(), root=url_for('get_fermentables')))

    return jsonify(hal.query(query, root=url_for('get_fermentables')))


@app.route('/hop', methods=['GET'])
@app.route('/hop/<id>', methods=['GET'])
def get_hops(id=None):
    query = db_session.query(models.Hop)

    if id:
        return jsonify(hal.item(query.filter_by(id=id).one(), root=url_for('get_hops')))

    return jsonify(hal.query(query, root=url_for('get_hops')))


@app.route('/recipe', methods=['GET'])
@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id=None):
    query = db_session.query(models.Recipe)

    if id:
        recipe = query.filter_by(id=id).one()
        result = hal.item(recipe, root=url_for('get_recipe'))
        result['profile'] = hal.item(recipe.profile, root='/profile')
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

    input = request.get_json()
    recipe.name = input['name']
    if input['profile']:
        recipe.profile = models.BrewingProfile(**input['profile'])
        recipe.profile.name = recipe.name

    session.commit()

    result = hal.item(recipe, root='/recipe')
    result['profile'] = hal.item(recipe.profile, root='/profile')
    return jsonify(result)


@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    db_session.query(models.Recipe).get(id).delete()
    db_session.commit()
    return get_recipe()



if __name__ == "__main__":
    app.run()

