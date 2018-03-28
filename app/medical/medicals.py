# @File    : medicals.py
# @author  : jack
# @software: PyCharm
# @datetime: 3/27  下午 14:34
import flask
from flask import flash, redirect, url_for, request, render_template
from sqlalchemy import or_
from app.public.decorators import login_required
from app.public.exts import db
from app.public.fenye import Pagination
from app.public.froms import Interface_yong_Form
from app.public.models import QuestionModel, Consultant, User, Medical
from app.public import config
from . import medical
@medical.route ('/detail3/')
@login_required
def detail():
    resylt = Medical.query.all()
    pager_obj = Pagination (request.args.get ("page", 1), len (resylt), request.path, request.args,
                            per_page_count=config.PageShow)
    index_list = resylt[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html ()
    return render_template ('medical/detail.html',html = html,index_list=index_list)
# 定义查看病例
@medical.route("/view/<int:id>/", methods=["GET"])
def user_view(id):
    view = Medical.query.filter_by (id=id).first ()
    return render_template("medical/Toview.html",views=view)
@medical.route ('/delete_case/<id>', methods=['GET', 'POST'])
def delete(id):
    next = request.headers.get ('Referer')
    testcase = Medical.query.filter_by (id=id).first ()
    db.session.delete (testcase)
    db.session.commit ()
    flash (u'删除成功')
    return redirect (next or url_for ('medical.detail'))

@medical.route ('/add_case/', methods=['GET', 'POST'])
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
            flash (u'添加档案成功')
            return redirect (url_for ('medical.detail'))
        except Exception as e:
            db.session.rollback ()
            flash (u'添加档案失败')
            return redirect (url_for ('medical.detail'))
    return flask.render_template ('medical/add.html', form=form, consultants=consultant)
    # return render_template ('health/add.html', form=form)


@medical.route ('/editor/<id>', methods=['GET', 'POST'])
def editor(id):
    next = request.headers.get ('Referer')
    consultant = Consultant.query.all ()
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
        # consultant_id = request.form.get ('consultant_id')
        health_consultant = request.form.get ('consultant')
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
        edit_case.consultant_id = health_consultant
        edit_case.outer_id = outer_id
        try:
            db.session.commit ()
            flash (u'编辑成功')
            return redirect (url_for ('medical.detail'))
        except:
            db.session.rollback ()
            flash (u'编辑失败，请重新编辑！')
            return flask.render_template ('medical/editor.html', edit=edit_case, consultants=consultant)
    return flask.render_template ('medical/editor.html', edit=edit_case, consultants=consultant)


@medical.route ('/search2/')
def search():
    q = flask.request.args.get ('q')
    questions = Medical.query.filter (or_ (Medical.medical_number.contains (q)))
    context = {
        'index_list': questions
    }
    return flask.render_template ('medical/detail.html', **context)
@medical.before_request
def before_request():
    id = flask.session.get('id')
    if id:
        user = User.query.get(id)
        flask.g.user = user
@medical.context_processor
def context_processor():
    if hasattr(flask.g,'user'):
        return {"user":flask.g.user}
    else:
        return {}