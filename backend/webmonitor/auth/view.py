from webmonitor.auth import auth_bp
from webmonitor import models
from webmonitor.models import PackagePeriodType
from flask import render_template, request, current_app, redirect, url_for
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.send_email import send_email
from datetime import datetime
from webmonitor.user.view import generate_invitation_code, add_invitation_bonus


# 用户注册
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    email       = request.form.get('email')
    password    = request.form.get('password')
    nickname    = request.form.get('nickname')
    code        = request.form.get('invitation_code')

    current_app.logger.info(f"user register with email={email}, password={password}, nickname={nickname}, invitation_code={code}")

    if not all([email, password, nickname]):
        abort(ErrorCode.PARAMS_INCOMPLETE)
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        abort(ErrorCode.PARAMS_INVALID, msg="邮箱格式错误")
    if len(password) < 4:
        abort(ErrorCode.PARAMS_INVALID, msg="密码长度不能小于4")
    if len(nickname) < 2:
        abort(ErrorCode.PARAMS_INVALID, msg="昵称长度不能小于2")

    # 检测邀请码是否有效
    if code is not None and code.strip() == '':
        code = None
    if code is not None:
        inviter = models.User.query.filter_by(inviter_code=code, is_deleted=0).first()
        if not inviter:
            abort(ErrorCode.INVITATION_CODE_INVALID)

    user = models.User.query.filter_by(email=email).first()
    # 用户已经存在并且已经激活
    if user and user.activated:
        abort(ErrorCode.USER_ALREADY_EXISTS)
    # 如果用户不存在则创建
    if not user:
        user = models.User(
            email=email, 
            password=password, 
            nickname=nickname, 
            role=0, 
            quota_exceeded=0,
            inviter_code=generate_invitation_code(),
            invitee_code=code,
        )
        models.db.session.add(user)
    # 如果用户存在则更新信息
    else:
        user.password = password
        user.nickname = nickname
        user.invitee_code = code
    models.db.session.commit()

    user = models.User.query.filter_by(email=email).first()

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

    current_app.logger.info(f"user activate with token={token}, user_id={user_id}")
    
    if not user_id:
        return abort(ErrorCode.TOKEN_INVALID)
    
    user = models.User.query.get(user_id)
    if not user:
        return abort(ErrorCode.USER_NOT_FOUND)
    if user.activated:
        return abort(ErrorCode.USER_ALREADY_ACTIVATED)
    
    # 检测邀请码是否有效
    if user.invitee_code is not None:
        inviter = models.User.query.filter_by(inviter_code=user.invitee_code, is_deleted=0).first()
        if not inviter:
            abort(ErrorCode.INVITATION_CODE_INVALID)
    
    # 激活用户
    user.activated = True
    user.activated_on = models.datetime.now()

    # 创建默认空间
    space = models.Space(name=f'默认空间', desc=f'用户{user.email}的默认空间', owner_id=user.id)
    models.db.session.add(space)

    # 添加默认套餐
    inital_templates = models.PackageTemplate.query.filter_by(is_deleted=0, initial=1).all()
    for template in inital_templates:
        current_app.logger.info(f"add initial package for user {user.id} with template {template.id}")
        package = models.Package(
            user_id                     = user.id,
            name                        = template.name,
            period_type                 = template.period_type,
            period_check_count          = template.period_check_count,
            price                       = template.price,
            start_time                  = datetime.now(),
            current_period_start_time   = datetime.now(),
            current_period_end_time     = PackagePeriodType.get_next_time(template.period_type, datetime.now()),
            check_count_left            = template.period_check_count,
            cancel_at_next              = 0,
            need_payment                = 0,
            is_last_payment_failed      = 0,
            stripe_payment_method_id    = None,
        )
        models.db.session.add(package)
    models.db.session.commit()

    user.check_quota()
    models.db.session.commit()

    # 添加邀请奖励
    if user.invitee_code is not None:
        add_invitation_bonus(inviter, user)

        invitation = models.UserInvitation(inviter_id=inviter.id, invitee_id=user.id, invitee_email=user.email)
        models.db.session.add(invitation)
        models.db.session.commit()
    
    url = current_app.config['FRONTEND_BASE_URL'] + '/activate_success'
    return redirect(url)
    

# 用户登录
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    email    = request.form.get('email')
    password = request.form.get('password')

    current_app.logger.info(f"user login with email={email}, password={password}")

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
    # if user.role != 0:
    #     return abort(ErrorCode.USER_NOT_FOUND)
    # 密码错误
    if not user.check_password(password):
        return abort(ErrorCode.PASSWORD_ERROR)
    # 用户未激活
    if not user.activated:
        return abort(ErrorCode.USER_NOT_FOUND)
    
    token = generate_token(user.id)
    return ok(data={
        'token': token,
        'role': user.role
    })


# 管理员登录
@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    email    = request.form.get('email')
    password = request.form.get('password')

    current_app.logger.info(f"admin login with email={email}, password={password}")

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
        return abort(ErrorCode.FORBIDDEN)
    
    token = generate_token(user.id)
    print(token)
    return ok(data={
        'token': token,
        'role': user.role
    })
