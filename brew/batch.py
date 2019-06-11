import sqlalchemy.exc

from datetime import datetime
from flask import jsonify, make_response, request

import models
import hal

from .app import app

from database import db_session
from user import get_logged_in_user, user_restrict


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
        return make_response(('Must supply recipe ID', 400))

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

