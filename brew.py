#!/usr/bin/env python3
from flask import Flask, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import zymurgy


app = Flask(__name__)


def get_session():
    engine = create_engine('sqlite:////var/www/brew/brew.sqlite3', echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


@app.route('/')
def home():
    return 'Brewtastic!'


@app.route('/fermentables', methods=['GET'])
def list_fermentables():
    session = get_session()
    fermentables = [zymurgy.Fermentable.from_model(fermentable)
                    for fermentable in session.query(models.Fermentable).all()]
    return jsonify([fermentable.params for fermentable in fermentables])


@app.route('/hops', methods=['GET'])
def list_hops():
    session = get_session()
    hops = [zymurgy.Hop.from_model(hop)
            for hop in session.query(models.Hop).all()]
    return jsonify([hop.params for hop in hops])


if __name__ == "__main__":
    app.run()
