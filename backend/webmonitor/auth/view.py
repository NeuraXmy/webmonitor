from webmonitor.auth import auth_bp
from webmonitor import models
from flask import render_template, request, current_app, redirect, url_for
from flask_restful import Resource
from webmonitor.utils.response import make_response
from webmonitor.utils.token import generate_token, verify_token
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from webmonitor.utils.email import send_email


# 用户注册
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    email       = request.form.get('email')
    password    = request.form.get('password')
    nickname    = request.form.get('nickname')
    if not all([email, password, nickname]):
        return make_response(400, msg="参数不完整")
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        return make_response(400, msg="邮箱格式错误")
    if len(password) < 4:
        return make_response(400, msg="密码长度不能小于4位")
    if len(nickname) < 2:
        return make_response(400, msg="昵称长度不能小于2位")

    user = models.User.query.filter_by(email=email).first()
    # 用户已激活
    if user and user.activated:
        return make_response(400, msg="用户已存在")
    # 如果用户不存在则创建
    if not user:
        user = models.User(email=email, password=password, nickname=nickname)
        models.db.session.add(user)
        models.db.session.commit()
    # 如果用户存在则更新信息
    else:
        user.password = password
        user.nickname = nickname
        models.db.session.commit()

    # 生成激活链接
    activation_token = generate_token(user.id)
    base_url = current_app.config['BACKEND_BASE_URL']
    activation_link = base_url + '/auth/activate?token=' + activation_token
    # 发送验证邮件
    send_email(user.email, 'webmonitor账户验证', 'email/activate.html', activation_link=activation_link)
    return make_response(200)
    

# 用户激活
@auth_bp.route('/auth/activate', methods=['GET'])
def activate():
    token = request.args.get('token')

    user_id = verify_token(token, 3600)
    if not user_id:
        return make_response(401, msg="token无效")
    
    user = models.User.query.get(user_id)
    if not user:
        return make_response(401, msg="用户不存在")
    if user.activated:
        return make_response(401, msg="用户已激活")
    
    try:
        # 激活用户
        user.activated = True
        user.activated_on = models.datetime.now()

        # 创建默认空间
        space = models.Space(name=f'默认空间', desc=f'用户{user.email}的默认空间', owner_id=user.id)
        models.db.session.add(space)

        models.db.session.commit()

    except Exception as e:
        return make_response(500)
    
    url = current_app.config['FRONTEND_BASE_URL'] + '/activate_success'
    return redirect(url)
    

# 用户登录
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    email    = request.form.get('email')
    password = request.form.get('password')
    if not all([email, password]):
        return make_response(400, msg="参数不完整")
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        return make_response(400, msg="邮箱格式错误")

    user = models.User.query.filter_by(email=email).first()
    # 用户不存在
    if not user:
        return make_response(400, msg="用户不存在")
    # 密码错误
    if not user.check_password(password):
        return make_response(400, msg="密码错误")
    # 用户未激活
    if not user.activated:
        return make_response(400, msg="用户未激活")
    
    token = generate_token(user.id)
    return make_response(200, data={'token': token})

