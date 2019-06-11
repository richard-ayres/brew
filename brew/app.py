import logging
import flask

logging.basicConfig(level=logging.INFO)

app = flask.Flask('brew.py')
app.secret_key = 'd58b39f5824fa132d1dd3582e2523d8240056ea4'

