from flask import Flask, render_template, request, redirect, flash, url_for, session
from exts import db
import flask
import config
from froms import RegistForm, Interface_yong_Form
from models import User, QuestionModel
from decorators import login_required
from sqlalchemy import or_
from fenye import Pagination
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app = Flask (__name__)
app.config.from_object(config)
db.init_app(app)
@app.route ('/index')
@login_required
def index():
    return flask.render_template('imdex.html')
@app.route('/detail/')
@login_required
def detail():
    resylt = QuestionModel.query.all()
    pager_obj = Pagination (request.args.get ("page", 1), len (resylt), request.path, request.args,
                            per_page_count=config.PageShow)
    index_list = resylt[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html ()
    return render_template ('detail2.html',html = html,index_list=index_list)
# @app.route('/login/',methods=['GET','POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         telephone = request.form.get ('telephone')
#         password = request.form.get ('password')
#         user = User.query.filter (User.telephone == telephone,User.password==password).first ()
#         if user:
#             flask.session['user_id']=user.id
#             # flask.session.permanent=True
#             #如果31不需要登录请设置该
#             return flask.redirect (flask.url_for ('index'))
#         else:
#             return '用户名或者密码错误'
@app.route('/login/',methods=['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        telephone = flask.request.form.get('telephone')
        password = flask.request.form.get('password')
        user = User.query.filter_by(telephone=telephone).first()
        if user and user.check_password(password):
            flask.session['id'] = user.id
            # flask.g.user = user
            return flask.redirect(flask.url_for('index'))
        else:
            return flask.redirect(flask.url_for('login'))

# @app.route ('/exti/',methods=['GET','POST'])
# def exti():
#     if request.method == 'GET':
#         return render_template ('regist.html')
#     else:
#         telephone=request.form.get('telephone')
#         username = request.form.get ('username')
#         password1 = request.form.get ('password1')
#         password2 = request.form.get ('password2')
#         #如果手机号码被注册就不能在进行注册
#         user=User.query.filter(User.telephone==telephone).first()
#         if user:
#             return  '手机号码已注册'
#         else:
#             if password1!=password2:
#                 return '密码不一致'
#             else:
#                 user=User(telephone=telephone,username=username,password=password1)
#                 print(user)
#                 db.session.add(user)
#                 db.session.commit()
#                 return redirect(url_for('login'))
@app.route('/regist/',methods=['GET','POST'])
def regist():
    if flask.request.method == 'GET':
        return flask.render_template('regist.html')
    else:
        form = RegistForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = User(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return flask.redirect(flask.url_for('login'))
        else:
            return ('注册失败')
@app.route('/logout/')
def logout():
    session.clear()
    # session.pop('user_id')
    return flask.redirect(flask.url_for('login'))
# @app.context_processor
# def my_context_procesor():
#     user_id=session.get('user_id')
#     if user_id:
#         user=User.query.filter(User.id == user_id).first()
#         if user:
#             return {'user':user}
#     return {}
@app.before_request
def before_request():
    id = flask.session.get('id')
    if id:
        user = User.query.get(id)
        flask.g.user = user
@app.context_processor
def context_processor():
    if hasattr(flask.g,'user'):
        return {"user":flask.g.user}
    else:
        return {}
@app.route('/delete_case/<id>',methods=['GET','POST'])
def delete(id):
    next = request.headers.get ('Referer')
    testcase = QuestionModel.query.filter_by (id=id).first()
    # testcase.status = True
    db.session.delete(testcase)
    db.session.commit ()
    flash (u'删除成功')
    return redirect (next or url_for ('detail'))
@app.route('/add_case/',methods=['GET','POST'])
def add_case():
    form = Interface_yong_Form ()
    if request.method == 'POST' :
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
        consultant_id = request.form.get ('consultant_id')
        outer_id=request.form.get('outer_id')
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
                                     consultant_id=consultant_id,
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
    return render_template ('add.html',form=form)
@app.route('/editor/<id>',methods=['GET','POST'])
def editor(id):
    next = request.headers.get ('Referer')
    edit_case = QuestionModel.query.filter_by (id=id).first()
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
            return render_template ('editor.html', edit=edit_case)
    return render_template ('editor.html', edit=edit_case)
@app.route('/search/')
def search():
    q = flask.request.args.get('q')
    questions = QuestionModel.query.filter(or_(QuestionModel.mobile.contains(q),QuestionModel.id_card.contains(q)))
    context = {
        'index_list': questions
    }
    return flask.render_template('detail2.html',**context)
if __name__ == '__main__':
    app.run ()