from webmonitor.auth import auth_bp
from webmonitor import models
from flask import render_template, request
from flask_restful import Resource
from webmonitor.utils.response import make_response
from webmonitor.utils.token import generate_token, verify_token
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from webmonitor.utils.email import send_email


# 注册表单
class RegistrationForm(FlaskForm):
    email       = StringField('Email', validators=[DataRequired(), Email()])
    password1   = PasswordField('Password', validators=[DataRequired()])
    password2   = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    nickname    = StringField('Nickname', validators=[DataRequired()])
    submit      = SubmitField('Register')


# 用户注册
@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        # 用户已激活
        if user and user.activated:
            return make_response(400, msg="用户已存在")
        # 如果用户不存在则创建
        if not user:
            user = models.User(email=form.email.data,
                            password=form.password1.data,
                            nickname=form.nickname.data)
            models.db.session.add(user)
            models.db.session.commit()
        # 如果用户存在则更新信息
        if user:
            user.password = form.password1.data
            user.nickname = form.nickname.data
            models.db.session.commit()
        # 生成激活链接
        activation_token = generate_token(user.id)
        activation_link = request.host_url + 'auth/activate/' + activation_token
        # 发送验证邮件
        send_email(user.email, 'webmonitor账户验证', 'email/activate.html', activation_link=activation_link)
        return make_response(200)
    
    else:
        return render_template('auth/register.html', form=form)


# 用户激活
@auth_bp.route('/activate/<token>', methods=['GET'])
def activate(token):
    user_id = verify_token(token, 3600)
    if not user_id:
        return make_response(401, msg="token无效")
    
    user = models.User.query.get(user_id)
    if not user:
        return make_response(401, msg="用户不存在")
    if user.activated:
        return make_response(401, msg="用户已激活")
    
    try:
        user.activated = True
        user.activated_on = models.datetime.now()
        models.db.session.add(user)
        models.db.session.commit()
    except Exception as e:
        return make_response(500)
    
    return make_response(200)


# 登录表单
class LoginForm(FlaskForm):
    email       = StringField('Email', validators=[DataRequired(), Email()])
    password    = PasswordField('Password', validators=[DataRequired()])
    submit      = SubmitField('Login')


# 用户登录
@auth_bp.route('/login', methods=['POST'])
def login():
    return {
        "status": 200,
        "msg": "登录成功",
        "data": {
            'token': "123456"
        }
    }
    form = request.form
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        # 用户不存在
        if not user:
            return make_response(400, msg="用户不存在")
        # 密码错误
        if not user.check_password(form.password.data):
            return make_response(400, msg="密码错误")
        # 用户未激活
        if not user.activated:
            return make_response(400, msg="用户未激活")
        
        token = generate_token(user.id)
        return make_response(200, data={'token': token})

    return make_response(400, msg="表单验证失败")


# 创建超级管理员

