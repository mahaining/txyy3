import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash

from app.public.exts import db


class User (db.Model):
    __tablename__ = "users"
    id = db.Column (db.String (100), primary_key=True, default=shortuuid.uuid)
    username = db.Column (db.String (100), nullable=False)
    telephone = db.Column (db.String (11), nullable=False)
    _password = db.Column (db.String (100), nullable=False)
    def __repr__(self):
        return "<telephone %r>" % self.telephone
    #
    # def __init__(self, *args, **kwargs):
    #     password = kwargs.pop ('password')
    #     username = kwargs.pop ('username')
    #     telephone = kwargs.pop ('telephone')
    #     self.password = password
    #     self.username = username
    #     self.telephone = telephone
    # #
    # @property
    # def password(self):
    #     return self._password
    #
    # @password.setter
    # def password(self, rawpwd):
    #     self._password = generate_password_hash (rawpwd)
    #
    # def check_password(self, rawpwd):
    #     return check_password_hash (self._password, rawpwd)

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self._password, pwd)  # 验证密码是否正确，返回True和False

class QuestionModel (db.Model):
    __tablename__ = 'health_record'
    id = db.Column (db.Integer, primary_key=True, autoincrement=True)  #
    user_id = db.Column (db.String (100), nullable=False)  # 用户id
    mobile = db.Column (db.String (200), nullable=False)  # 用户手机号
    real_name = db.Column (db.String (200), nullable=False)  # 姓名
    id_card = db.Column (db.String (100), nullable=False)  # 身份证号
    age = db.Column (db.String (100), nullable=False)  # 年龄
    sex = db.Column (db.String (100), nullable=False)  # '1:男;2:女;0:未知',
    weight = db.Column (db.String (200), nullable=False)  # 体重
    height = db.Column (db.String (200), nullable=False)  # 身高
    remark = db.Column (db.String (300), nullable=False)  # 备注
    consultant_id = db.Column (db.String (30), db.ForeignKey ('health_consultant.id'))  # 医顾id
    # create_at=db.Column(db.Integer,nullable=False)#创建时间
    # update_at=db.Column(db.Integer,nullable=False)#修改时间
    outer_id = db.Column (db.String (30), nullable=False)  # 第三方id
    # outer_consultant_id=db.Column(db.Integer,nullable=False)#第三方顾问id
    # outer = db.relationship ('User', backref='health_record')
    Medical = db.relationship ('Medical', backref='health_record')

class Consultant (db.Model):
    __tablename__ = 'health_consultant'
    id = db.Column (db.Integer (), primary_key=True)
    name = db.Column (db.String (), unique=True)
    phone = db.Column (db.String (), nullable=False)
    status = db.Column (db.String (), nullable=False)
    outer_id = db.Column (db.String (), nullable=False)
    QuestionModels = db.relationship ('QuestionModel', backref='health_consultant')
    def __repr__(self):
        return self.name

from . import login_manager
@login_manager.user_loader
def load_user(user_id):     
    return User.query.get (int (user_id))
class Medical (db.Model):
    __tablename__ = 'medical_record'
    id = db.Column (db.Integer, primary_key=True, autoincrement=True)  #
    medical_number = db.Column (db.String (100), nullable=False)  # 就诊号
    medical_type = db.Column (db.String (200), nullable=False)  # '就诊类型 0:初诊；1:复诊',
    medical_time = db.Column (db.String (200), nullable=False)  # 就诊时间',
    complaint = db.Column (db.String (100), nullable=False)  # 主诉
    diagnostic = db.Column (db.String (100), nullable=False)  # 诊断意见
    treatment = db.Column (db.String (100), nullable=False)  # 治疗意见',
    health_record_id = db.Column (db.String (200),  db.ForeignKey ('health_record.id'))  # 患者档案id
    allergy_history = db.Column (db.String (200), nullable=False)  # 过敏史
    prescription_type = db.Column (db.String (300), nullable=False)  # '处方类型 0:普通处方;1:急诊处方;2:麻醉处方',
    outer_doctor_id = db.Column (db.String (30), nullable=False)  # 存在第三方的医生id
    outer_health_record_id = db.Column (db.String (30), nullable=False)  # 存在第三方的患者id
    status=db.Column(db.Integer,nullable=False)#状态 0:未开始;1:已登记;2:已挂号;3:已开病历;4
    outer_id = db.Column (db.Integer, nullable=False)  # 存在第三方的病历id