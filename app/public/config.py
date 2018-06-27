import os

HOSTNAME = 'xxx'
PORT = '3306'
DATABASE = 'xxx'
USERNAME = 'xxx'
PASSWORD = 'xxx'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format (USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
DEBUG = True
SECRET_KEY = os.urandom (24)
SQLALCHEMY_ECHO = True
PageShow = 30  # 这里配置的就是每个页显示多少
SQLALCHEMY_TRACK_MODIFICATIONS = True
