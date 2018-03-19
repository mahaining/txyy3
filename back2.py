import mysql
from flask import Flask, request, render_template, session
from exts import db
import flask
import config
from froms import RegistForm
from models import User
from decorators import login_required
from sqlalchemy import or_

app = Flask (__name__)
app.config.from_object(config)
db.init_app(app)
@app.route ('/index')
def index():
    return flask.render_template('imdex.html')
@app.route('/detail/')
def detail():
    test = mysql.get_query_db ("SELECT id,user_id,mobile,real_name,id_card,age FROM health_record;")
    return render_template ('detail.html', index_list=test)
@app.route ('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get ('telephone')
        password = request.form.get ('password')
        user = User.query.filter (User.telephone == telephone,User.password==password).first ()
        if user:
            flask.session['user_id']=user.id
            flask.session.permanent=True
            #如果31不需要登录请设置该
            return flask.redirect (flask.url_for ('index'))
        else:
            return '用户名或者密码错误'
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
            user = User.query.filter (User.telephone == telephone).first ()
            if user:
                return  '手机号码已注册'
            else:
                user = User(telephone=telephone,username=username,password=password)
                db.session.add(user)
                db.session.commit()
                return flask.redirect(flask.url_for('login'))
        else:
            return u'注册失败'
@app.route('/logout/')
def logout():
    session.clear()
    # session.pop('user_id')
    return flask.redirect(flask.url_for('login'))
@app.context_processor
def my_context_procesor():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}
if __name__ == '__main__':
    app.run ()
