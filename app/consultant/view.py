import flask
from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import or_
from app.public import config
from app.public.fenye import Pagination
from app.public.froms import Interface_consultant
from app.public.models import Consultant, QuestionModel
from . import consultant
from app.public.exts import db

@consultant.route ('/detail2/')
# @login_required
def detail():
    resylt = Consultant.query.all()
    pager_obj = Pagination (request.args.get ("page", 1), len (resylt), request.path, request.args,
                            per_page_count=config.PageShow)
    index_list = resylt[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html ()
    return render_template ('consultant/detail.html', html=html, index_list=index_list)


@consultant.route ('/delete_consultant/<id>', methods=['GET', 'POST'])
def delete(id):
    next = request.headers.get ('Referer')
    testcase = Consultant.query.filter_by (id=id).first ()
    db.session.delete (testcase)
    db.session.commit ()
    flash (u'删除成功')
    return redirect (next or url_for ('consultant.detail'))


@consultant.route ('/add_consultant/', methods=['GET', 'POST'])
def add_case():
    form = Interface_consultant ()
    if request.method == 'POST':
        name = request.form.get ('name')
        phone = request.form.get ('phone')
        status = request.form.get ('status')
        outer_id = request.form.get ('outer_id')
        try:
            newcase = Consultant (
                name=name,
                phone=phone,
                status=status,
                outer_id=outer_id,
            )
            db.session.add (newcase)
            db.session.commit ()
            flash (u'添加医顾成功')
            return redirect (url_for ('consultant.detail'))
        except Exception as e:
            db.session.rollback ()
            flash (u'添加医顾失败')
            return redirect (url_for ('consultant.detail'))
    return render_template ('consultant/add.html', form=form)


@consultant.route ('/consultant/<id>', methods=['GET', 'POST'])
def editor(id):
    next = request.headers.get ('Referer')
    edit_case = Consultant.query.filter_by (id=id).first ()
    if request.method == 'POST':
        name = request.form.get ('name')
        phone = request.form.get ('phone')
        status = request.form.get ('status')
        outer_id = request.form.get ('outer_id')

        edit_case.name = name
        edit_case.phone = phone
        edit_case.status = status
        edit_case.outer_id = outer_id

        try:
            db.session.commit ()
            flash (u'修改成功')
            return redirect (url_for ('consultant.detail'))
        except:
            db.session.rollback ()
            flash (u'修改失败，请重新编辑！')
            return render_template ('consultant/edutor.html', edit=edit_case)
    return render_template ('consultant/edutor.html', edit=edit_case)


@consultant.route ('/search/')
def search():
    q = flask.request.args.get ('q')
    questions = Consultant.query.filter (or_ (Consultant.phone.contains (q), Consultant.name.contains (q)))
    context = {
        'index_list': questions
    }
    return flask.render_template ('consultant/detail.html', **context)
