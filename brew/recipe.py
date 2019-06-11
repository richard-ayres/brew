import logging
import sqlalchemy.orm.exc
import sqlalchemy.exc

from flask import jsonify, make_response, request

import zymurgy
import calculators
import models
import hal

from .app import app

from database import db_session
from user import get_logged_in_user, user_restrict


def load_recipe(id):
    """Convenience function to load the recipe given the ID"""
    query = user_restrict(db_session.query(models.Recipe), models.UserRecipeLink)
    return query.filter(models.Recipe.id==id).one()


@app.route('/recipe', methods=['GET'])
@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id=None):
    if id is None:
        # We're fetch the list of recipes
        query = user_restrict(db_session.query(models.Recipe), models.UserRecipeLink)
        return jsonify(hal.query(query, href='/recipe'))

    try:
        recipe = load_recipe(id)
        result = hal.item(recipe, href='/recipe/{id}', stats='/recipe/{id}/stats')
        result['profile'] = hal.item(recipe.profile, href='/recipe/{id}/profile'.format(id=id))
        result['grain_bill'] = hal.item(recipe.grain_bill, href='/recipe/{id}/grain_bill'.format(id=id))
        result['hop_schedule'] = hal.item(recipe.hop_schedule, href='/recipe/{id}/hop_schedule'.format(id=id))
        if recipe.yeast:
            result['yeast'] = hal.item(recipe.yeast, href='/yeast/{id}'.format(id=recipe.yeast_id))
        return jsonify(result)

    except sqlalchemy.orm.exc.NoResultFound:
        return make_response(('Recipe not found', 404))


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

        recipe.yeast_id = req.get('yeast', None)

        user = get_logged_in_user()
        db_session.add(models.UserProfileLink(user=user, profile=recipe.profile))
        db_session.add(models.UserRecipeLink(user=user, recipe=recipe))

        db_session.commit()

    except sqlalchemy.exc.IntegrityError as ex:
        db_session.rollback()
        return make_response(('Error with recipe: {}'.format(ex), 400))

    except sqlalchemy.orm.exc.NoResultFound as ex:
        db_session.rollback()
        return make_response(('Item not found: {}'.format(ex), 404))

    result = hal.item(recipe, href='/recipe/{id}'.format(id=recipe.id), stats='/recipe/{id}/stats')
    result['profile'] = hal.item(recipe.profile, href='/recipe/{id}/profile'.format(id=recipe.id))
    result['grain_bill'] = hal.item(recipe.grain_bill, href='/recipe/{id}/grain_bill'.format(id=recipe.id))
    result['hop_schedule'] = hal.item(recipe.hop_schedule, href='/recipe/{id}/hop_schedule'.format(id=recipe.id))
    if recipe.yeast:
        result['yeast'] = hal.item(recipe.yeast, href='/yeast/{id}'.format(id=recipe.yeast_id))

    return jsonify(result)


@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    try:
        recipe = load_recipe(id)

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
        recipe = load_recipe(id)
        return jsonify(hal.item(recipe.profile, href='/profile/{id}'.format(id=recipe.profile_id)))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Recipe not found', 404))


@app.route('/recipe/<id>/hop_schedule', methods=['GET'])
def get_recipe_hop_schedule(id):
    try:
        recipe = load_recipe(id)
        return jsonify(hal.item(recipe.hop_schedule, href='/recipe/{recipe_id}/hop_schedule'.format(recipe_id=id)))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Recipe not found', 404))


@app.route('/recipe/<id>/grain_bill', methods=['GET'])
def get_recipe_grain_bill(id):
    try:
        recipe = load_recipe(id)
        return jsonify(hal.item(recipe.grain_bill, href='/recipe/{recipe_id}/grain_bill'.format(recipe_id=id)))

    except sqlalchemy.orm.exc.NoResultFound:
        db_session.rollback()
        return make_response(('Recipe not found', 404))



@app.route('/recipe/<id>/stats')
def get_recipe_stats(id):
    try:
        result = dict()

        recipe = load_recipe(id)

        def load_fermentable(gb):
            fermentable = zymurgy.Fermentable.from_model(gb.fermentable)
            fermentable['weight'] = gb.weight
            if gb.ebc:
                fermentable['ebc'] = gb.ebc
            if gb.extract_max:
                fermentable['extract-max'] = gb.extract_max
            if gb.fermentability:
                fermentable['fermentability'] = gb.fermentability
            return fermentable

        def load_hop(h):
            if h.when not in {'fwh', 'boil'} or h.boil_time is None or h.boil_time == 0:
                return None
            hop = zymurgy.Hop.from_model(h.hop)
            hop['weight'] = h.weight
            hop['boil-time'] = h.boil_time
            if h.alpha:
                hop['alpha'] = h.alpha
            return hop


        fermentables = list(filter(None, map(load_fermentable, recipe.grain_bill)))
        hops = list(filter(None, map(load_hop, recipe.hop_schedule)))

        gb = calculators.GrainBill(
            efficiency=recipe.profile.mash_efficiency,
            volume=recipe.profile.volume_in_fermenter,
            fermentables=fermentables
        )

        og, ebc = gb.calculate()
        result['og'] = og
        result['ebc'] = ebc

        attenuation = calculators.Attenuation(
            brew_efficiency=recipe.profile.mash_efficiency,
            original_gravity=og,
            fermentables=fermentables,
            volume=recipe.profile.volume_in_fermenter
        )
        # if recipe.yeast:
        #     attenuation['yeast-efficiency'] = recipe.yeast.attenuation
        result['fg'] = attenuation.calculate()

        hop_schedule = calculators.HopSchedule(
            gravity=og,
            volume=recipe.profile.volume_in_fermenter,
            hop_additions=hops
        )
        result['ibu'] = hop_schedule.calculate()

        result['abv'] = calculators.ABVCalculator(original_gravity=result['og'], final_gravity=result['fg']).calculate()

        return jsonify(hal.item(result, href='/recipe/{id}/stats'.format(id=recipe.id), recipe='/recipe/{id}'.format(id=recipe.id)))
    except sqlalchemy.orm.exc.NoResultFound:
        return make_response(('Recipe not found', 404))

