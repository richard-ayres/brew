import sqlalchemy.exc

from flask import jsonify, make_response, request

import models
import hal

from .app import app

from database import db_session
from user import get_logged_in_user, user_restrict


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


