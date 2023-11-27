from webmonitor.auth import auth_bp
from webmonitor import models
from flask import render_template, request, current_app, redirect, url_for
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email


# 用户注册
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    email       = request.form.get('email')
    password    = request.form.get('password')
    nickname    = request.form.get('nickname')
    if not all([email, password, nickname]):
        abort(ErrorCode.PARAMS_INCOMPLETE)
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        abort(ErrorCode.PARAMS_INVALID, msg="邮箱格式错误")
    if len(password) < 4:
        abort(ErrorCode.PARAMS_INVALID, msg="密码长度不能小于4")
    if len(nickname) < 2:
        abort(ErrorCode.PARAMS_INVALID, msg="昵称长度不能小于2")

    user = models.User.query.filter_by(email=email).first()
    # 用户已经存在并且已经激活
    if user and user.activated:
        abort(ErrorCode.USER_ALREADY_EXISTS)
    # 如果用户不存在则创建
    if not user:
        user = models.User(email=email, password=password, nickname=nickname, role=0)
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
    return ok()
    

# 用户激活
@auth_bp.route('/auth/activate', methods=['GET'])
def activate():
    token = request.args.get('token')

    user_id = verify_token(token, 3600)
    if not user_id:
        return abort(ErrorCode.TOKEN_INVALID)
    
    user = models.User.query.get(user_id)
    if not user:
        return abort(ErrorCode.USER_NOT_FOUND)
    if user.activated:
        return abort(ErrorCode.USER_ALREADY_ACTIVATED)
    
    # 激活用户
    user.activated = True
    user.activated_on = models.datetime.now()

    # 创建默认空间
    space = models.Space(name=f'默认空间', desc=f'用户{user.email}的默认空间', owner_id=user.id)
    models.db.session.add(space)

    models.db.session.commit()
    
    url = current_app.config['FRONTEND_BASE_URL'] + '/activate_success'
    return redirect(url)
    

# 用户登录
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    email    = request.form.get('email')
    password = request.form.get('password')
    if not all([email, password]):
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        return abort(ErrorCode.PARAMS_INVALID, msg="邮箱格式错误")

    user = models.User.query.filter_by(email=email).first()
    # 用户不存在
    if not user:
        return abort(ErrorCode.USER_NOT_FOUND)
    # 不是普通用户
    if user.role != 0:
        return abort(ErrorCode.USER_NOT_FOUND)
    # 密码错误
    if not user.check_password(password):
        return abort(ErrorCode.PASSWORD_ERROR)
    # 用户未激活
    if not user.activated:
        return abort(ErrorCode.USER_NOT_FOUND)
    
    token = generate_token(user.id)
    return ok(data={'token': token})

@auth_bp.route('/admin/login', methods=['POST'])
def login():
    email    = request.form.get('email')
    password = request.form.get('password')
    if not all([email, password]):
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        return abort(ErrorCode.PARAMS_INVALID, msg="邮箱格式错误")
    
    user = models.User.query.filter_by(email=email).first()
    # 用户不存在
    if not user:
        return abort(ErrorCode.USER_NOT_FOUND)
    # 密码错误
    if not user.check_password(password):
        return abort(ErrorCode.PASSWORD_ERROR)
    # 不是管理员
    if user.role != 1:
        return abort(ErrorCode.USER_NOT_FOUND)
    
    token = generate_token(user.id)
    return ok(data={'token': token})