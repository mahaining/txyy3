import os
HOSTNAME = '120.78.206.186'
PORT     = '3306'
DATABASE = 'txyy_customer'
USERNAME = 'tecker'
PASSWORD = 'tck@2017'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
DEBUG=True
SECRET_KEY = os.urandom(24)
SQLALCHEMY_ECHO = True
PageShow=5#这里配置的就是每个页显示多少
