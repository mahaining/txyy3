import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash

from public.exts import db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    username = db.Column(db.String(100),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    _password = db.Column(db.String(100),nullable=False)

    def __init__(self,*args,**kwargs):
        password = kwargs.pop('password')
        username = kwargs.pop('username')
        telephone = kwargs.pop('telephone')
        self.password = password
        self.username = username
        self.telephone = telephone

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_password(self,rawpwd):
        return check_password_hash(self._password,rawpwd)

class QuestionModel(db.Model):
    __tablename__ = 'health_record'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)#
    user_id=db.Column(db.String(100),nullable=False)#用户id
    mobile = db.Column (db.String (200), nullable=False)#用户手机号
    real_name = db.Column (db.String (200), nullable=False)#姓名
    id_card=db.Column(db.String(100),nullable=False)#身份证号
    age=db.Column(db.String(100),nullable=False)#年龄
    sex=db.Column(db.String(100),nullable=False)#'1:男;2:女;0:未知',
    weight = db.Column (db.String (200), nullable=False)#体重
    height = db.Column (db.String (200), nullable=False)#身高
    remark = db.Column(db.String(300),nullable=False)#备注
    consultant_id=db.Column(db.String(30),db.ForeignKey('health_consultant.id'))#医顾id
    # create_at=db.Column(db.Integer,nullable=False)#创建时间
    # update_at=db.Column(db.Integer,nullable=False)#修改时间
    outer_id=db.Column(db.String(30),nullable=False)#第三方id
    # outer_consultant_id=db.Column(db.Integer,nullable=False)#第三方顾问id
    # outer = db.relationship ('User', backref='health_record')
class Consultant(db.Model):
    __tablename__='health_consultant'
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(),unique=True)
    def __repr__(self):
        return  self.name