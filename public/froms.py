import wtforms
from flask_wtf import Form
from wtforms import validators, StringField


class RegistForm (wtforms.Form):
    telephone = wtforms.StringField (validators=[validators.length (min=11, max=11)])
    username = wtforms.StringField (validators=[validators.InputRequired (message=u'请输入用户名')])
    password1 = wtforms.StringField (validators=[validators.InputRequired ()])
    password2 = wtforms.StringField (validators=[validators.InputRequired (), validators.EqualTo ('password1')])


class Interface_yong_Form (Form):
    user_id = StringField (u'用户ID', [validators.DataRequired ()], render_kw={'placeholder': u'请输入用户ID'})
    mobile = StringField (u'患者手机号', [validators.DataRequired ()], render_kw={'placeholder': u'请输入患者手机号'})
    real_name = StringField (u'患者姓名', [validators.DataRequired ()], render_kw={'placeholder': u'请输入患者姓名'})
    id_card = StringField (u'患者身份证号码', [validators.DataRequired ()], render_kw={'placeholder': u'请输入 患者身份证号码'})
    age = StringField (u'年龄', [validators.DataRequired ()], render_kw={'placeholder': u'请输入年龄'})
    # sex = StringField (u'性别', [validators.DataRequired ()], render_kw={'placeholder': u'请输入性别'})
    weight = StringField (u'体重', [validators.DataRequired ()], render_kw={'placeholder': u'请输入体重'})
    height = StringField (u'身高', [validators.DataRequired ()], render_kw={'placeholder': u'请输入身高'})
    remark = StringField (u'备注', [validators.DataRequired ()], render_kw={'placeholder': u'备注'})
    # consultant_id = StringField (u'第三方ID', [validators.DataRequired ()], render_kw={'placeholder': u'第三方ID'})
    outer_id = StringField (u'ID', [validators.DataRequired ()], render_kw={'placeholder': u'id'})
