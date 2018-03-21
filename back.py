from flask import Flask, render_template, request, redirect, flash, url_for, session
from public.exts import db
import flask
from public import config
from public.froms import RegistForm, Interface_yong_Form
from public.models import User, QuestionModel, Consultant
from sqlalchemy import or_
from public.fenye import Pagination
app = Flask (__name__)
app.config.from_object (config)
db.init_app (app)


@app.route ('/index')
# @login_required
def index():
    return flask.render_template ('public/imdex.html')
@app.route ('/detail/')
# @login_required
def detail():
    resylt = QuestionModel.query.all ()
    pager_obj = Pagination (request.args.get ("page", 1), len (resylt), request.path, request.args,
                            per_page_count=config.PageShow)
    index_list = resylt[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html ()
    return render_template ('health/detail.html', html=html, index_list=index_list)

@app.route ('/delete_case/<id>', methods=['GET', 'POST'])
def delete(id):
    next = request.headers.get ('Referer')
    testcase = QuestionModel.query.filter_by (id=id).first ()
    # testcase.status = True
    db.session.delete (testcase)
    db.session.commit ()
    flash (u'删除成功')
    return redirect (next or url_for ('detail'))


@app.route ('/add_case/', methods=['GET', 'POST'])
def add_case():
    form = Interface_yong_Form ()
    consultant = Consultant.query.all ()
    if request.method == 'POST':
        # id = request.form.get ('id')
        user_id = request.form.get ('user_id')
        mobile = request.form.get ('mobile')
        real_name = request.form.get ('real_name')
        id_card = request.form.get ('id_card')
        age = request.form.get ('age')
        sex = request.form.get ('sex')
        weight = request.form.get ('weight')
        height = request.form.get ('height')
        remark = request.form.get ('remark')
        health_consultant = request.form.get ('consultant')
        # consultant_id= request.form.get ('consultant_id')
        outer_id = request.form.get ('outer_id')
        try:
            newcase = QuestionModel (
                user_id=user_id,
                mobile=mobile,
                real_name=real_name,
                id_card=id_card,
                age=age,
                sex=sex,
                weight=weight,
                height=height,
                remark=remark,
                consultant_id=health_consultant,
                # consultant_id=consultant_id,
                outer_id=outer_id
            )
            db.session.add (newcase)
            db.session.commit ()
            flash (u'添加用例成功')
            return redirect (url_for ('detail'))
        except Exception as e:
            db.session.rollback ()
            flash (u'添加用例失败')
            return redirect (url_for ('detail'))
    return render_template ('health/add.html', form=form,consultants=consultant)
    # return render_template ('health/add.html', form=form)


@app.route ('/editor/<id>', methods=['GET', 'POST'])
def editor(id):
    next = request.headers.get ('Referer')
    edit_case = QuestionModel.query.filter_by (id=id).first ()
    if request.method == 'POST':
        user_id = request.form.get ('user_id')
        mobile = request.form.get ('mobile')
        real_name = request.form.get ('real_name')
        id_card = request.form.get ('id_card')
        age = request.form.get ('age')
        sex = request.form.get ('sex')
        weight = request.form.get ('weight')
        height = request.form.get ('height')
        remark = request.form.get ('remark')
        consultant_id = request.form.get ('consultant_id')
        outer_id = request.form.get ('outer_id')

        edit_case.user_id = user_id
        edit_case.mobile = mobile
        edit_case.real_name = real_name
        edit_case.id_card = id_card
        edit_case.age = age
        edit_case.sex = sex
        edit_case.weight = weight
        edit_case.height = height
        edit_case.remark = remark
        edit_case.consultant_id = consultant_id
        edit_case.outer_id = outer_id
        try:
            db.session.commit ()
            flash (u'编辑成功')
            return redirect (url_for ('detail'))
        except:
            db.session.rollback ()
            flash (u'编辑失败，请重新编辑！')
            return render_template ('health/editor.html', edit=edit_case)
    return render_template ('health/editor.html', edit=edit_case)


@app.route ('/search/')
def search():
    q = flask.request.args.get ('q')
    questions = QuestionModel.query.filter (or_ (QuestionModel.mobile.contains (q), QuestionModel.id_card.contains (q)))
    context = {
        'index_list': questions
    }
    return flask.render_template ('health/detail.html', **context)
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
            flask.g.user = user
            return flask.redirect (flask.url_for ('index'))
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
if __name__ == '__main__':
    app.run ()
