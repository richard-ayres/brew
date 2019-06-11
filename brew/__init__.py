from flask import redirect

from .app import app

import brew.user
import brew.recipe
import brew.batch
import brew.ingredients


@app.route('/')
def home():
    return redirect('/index.html')


