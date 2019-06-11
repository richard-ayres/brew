import sqlalchemy.orm.exc
import sqlalchemy.exc
import hashlib
import datetime

from flask import make_response, request, session, redirect

import models

from .app import app

from database import db_session


def random_bytes(length):
    return open('/dev/urandom', 'rb').read(length)


@app.route('/user/login', methods=["POST"])
def user_login():
    try:
        email = request.form['email']
        password = request.form['password']

        user = db_session.query(models.User).filter_by(email=email, active=True).one()

        m = hashlib.sha256()
        m.update(user.salt.encode('utf-8'))
        m.update(password.encode('utf-8'))

        if m.hexdigest() != user.password:
            return make_response(('Login failed', 401))

        session['user_id'] = user.id

        user.last_login = datetime.datetime.now()
        db_session.commit()

        return make_response(('Success', 200))

    except KeyError:
        return make_response(('Invalid login data', 400))

    except sqlalchemy.orm.exc.NoResultFound:
        return make_response(('Login failed', 401))


@app.route('/user/login', methods=["GET"])
def user_login_page():
    return make_response("""
<html><head><title>Login</title></head>
<body>
    <form method="POST">
        <label for="email">Email: <input id="email" name="email"></label>
        <label for="password">Password: <input id="password" name="password" type="password"></label>
        <input type="submit" value="Login">
    </form>
</body>
</html>""")


@app.route('/user/logout', methods=["GET"])
def user_logout():
    session.pop('user_id')
    return redirect('/user/login')


@app.route('/user/register', methods=["POST"])
def user_register():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        check_password = request.form['check_password']

        if password != check_password:
            return make_response(('Passwords do not match', 400))

        user = models.User(email=email, name=name)

        m = hashlib.sha256()
        m.update(random_bytes(64))
        user.salt = m.hexdigest()

        m = hashlib.sha256()
        m.update(user.salt.encode('utf-8'))
        m.update(password.encode('utf-8'))
        user.password = m.hexdigest()

        db_session.add(user)
        db_session.commit()

        return make_response(('Success', 200))
    except KeyError:
        return make_response(('Invalid data', 400))

    except sqlalchemy.exc.IntegrityError:
        return make_response(('User already exists', 400))

