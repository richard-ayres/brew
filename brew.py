#!/usr/bin/env python3
import os.path
import logging

from flask import Flask, jsonify, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import zymurgy
import hal


app = Flask(__name__)


DOCROOT = os.path.dirname(__file__)


def get_session():
    engine = create_engine('sqlite:////var/www/brew/brew.sqlite3', echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


@app.route('/')
def home():
    return redirect('/index.html')


@app.route('/fermentable', methods=['GET'])
@app.route('/fermentable/<name>', methods=["GET"])
def get_fermentables(name=None):
    session = get_session()
    query = session.query(models.Fermentable)

    if name:
        return jsonify(hal.item(query.filter_by(name=name).one(), root=url_for('get_fermentables')))

    return jsonify(hal.query(query, root=url_for('get_fermentables')))


@app.route('/hop', methods=['GET'])
@app.route('/hop/<name>', methods=['GET'])
def get_hops(name=None):
    session = get_session()
    query = session.query(models.Hop)

    if name:
        return jsonify(hal.item(query.filter_by(name=name).one(), root=url_for('get_hops')))

    return jsonify(hal.query(query, root=url_for('get_hops')))


if __name__ == "__main__":
    app.run()

