from functools import wraps
import flask
def login_required(func):
    @wraps (func)
    def wrapper(*args, **kwargs):
        if hasattr (flask.g, 'user'):
            return func (*args, **kwargs)
        else:
            return flask.redirect (flask.url_for ('user.login'))

    return wrapper
# 定义登录判断装饰器
# from flask import session, redirect, url_for, request
#
#
# def user_login_req(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         # session不存在时请求登录
#         if "user" not in session:
#             return redirect(url_for("home.login", next=request.url))
#         return f(*args, **kwargs)
#
#     return decorated_function