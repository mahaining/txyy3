from flask import render_template, session, redirect, url_for, request, flash

from app.public.decorators import login_required
from app.public.exts import db
from app.public.froms import RegistForm
# from app.public.froms import  LoginForm
from app.public.models import User
from . import user
import flask
@user.route ('/index')
@login_required
def index():
    return flask.render_template ('index/index.html')
@user.route ('/back')
@login_required
def back():
    return flask.render_template ('public/back.html')
@user.route ('/login/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template ('login/login.html')
    else:
        telephone = flask.request.form.get ('telephone')
        password = flask.request.form.get ('password')
        user = User.query.filter_by (telephone=telephone).first ()
        if user and user.check_pwd (password):
            flask.session['id'] = user.id
            flask.g.user = user
            return flask.redirect (flask.url_for ('user.index'))
        else:
            return flask.redirect (flask.url_for ('user.login'))
@user.route ('/regist/', methods=['GET', 'POST'])
def regist():
    if flask.request.method == 'GET':
        return flask.render_template ('login/regist.html')
    else:
        form = RegistForm (flask.request.form)
        # if form.validate ():
        #     telephone = form.telephone.data
        #     username = form.username.data
        #     password = form.password1.data
        if form.validate ():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = User (telephone=telephone, username=username, password=password)
            db.session.add (user)
            db.session.commit ()
            return flask.redirect (flask.url_for ('user.login'))
        else:
            return ('注册失败')


@user.route ('/logout/')
def logout():
    session.clear ()
    # session.pop('user_id')
    return flask.redirect (flask.url_for ('user.login'))


@user.before_request
def before_request():
    id = flask.session.get ('id')
    if id:
        user = User.query.get (id)
        flask.g.user = user


@user.context_processor
def context_processor():
    if hasattr (flask.g, 'user'):
        return {"user": flask.g.user}
    else:
        return {}