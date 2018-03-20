import flask
from flask import session, Blueprint, app, render_template
from public.exts import db
from public.froms import RegistForm
from public.models import User
from flask import Flask
app = Flask (__name__)
user1 = Blueprint ('login', __name__)
@app.route ('/login/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template ('login/login.html')
    else:
        telephone = flask.request.form.get ('telephone')
        password = flask.request.form.get ('password')
        user = User.query.filter_by (telephone=telephone).first ()
        if user and user.check_password (password):
            flask.session['id'] = user.id
            # flask.g.user = user
            # return flask.redirect (flask.url_for ('index'))
        else:
            return flask.redirect (flask.url_for ('login'))


@app.route ('/regist/', methods=['GET', 'POST'])
def regist():
    if flask.request.method == 'GET':
        return flask.render_template ('login/regist.html')
    else:
        form = RegistForm (flask.request.form)
        if form.validate ():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = User (telephone=telephone, username=username, password=password)
            db.session.add (user)
            db.session.commit ()
            return flask.redirect (flask.url_for ('login'))
        else:
            return ('注册失败')


@app.route ('/logout/')
def logout():
    session.clear ()
    # session.pop('user_id')
    return flask.redirect (flask.url_for ('login'))


@app.before_request
def before_request():
    id = flask.session.get ('id')
    if id:
        user = User.query.get (id)
        flask.g.user = user


@app.context_processor
def context_processor():
    if hasattr (flask.g, 'user'):
        return {"user": flask.g.user}
    else:
        return {}
