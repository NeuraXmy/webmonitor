from webmonitor.user import user_bp
from webmonitor import models
from flask import render_template, request, current_app
from flask_restful import Resource
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.send_email import send_email
from webmonitor.utils.auth import login_required
import webmonitor.utils.watch as watch_utils
from webmonitor.utils.page import paginate
from random import randint
from datetime import datetime
from webmonitor.models import PackagePeriodType

# 生成邀请码
def generate_invitation_code():
    # 随机24个字符a-zA-Z
    code = ''
    for i in range(20):
        code += chr(randint(65, 90) if randint(0, 1) else randint(97, 122))
    return code


# 添加邀请奖励
def add_invitation_bonus(inviter, invitee):
    inviter_templates = models.PackageTemplate.query.filter_by(is_deleted=0, inviter_package=1).all()
    for template in inviter_templates:
        current_app.logger.info(f"add inviter bonus for user {inviter.id} with template {template.id}")
        package = models.Package(
            user_id                     = inviter.id,
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

    invitee_templates = models.PackageTemplate.query.filter_by(is_deleted=0, invitee_package=1).all()
    for template in invitee_templates:
        current_app.logger.info(f"add invitee bonus for user {invitee.id} with template {template.id}")
        package = models.Package(
            user_id                     = invitee.id,
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

    invitee.check_quota()
    inviter.check_quota()
    models.db.session.commit()


# 用户获取自己信息
@user_bp.route('/user', methods=['GET'])
@login_required
def get_user_info(user):
    current_app.logger.info(f"user get info with user_id={user.id}")

    ret = {
        'id': user.id,
        'email': user.email,
        'nickname': user.nickname,
        'create_time': user.create_time,
        'update_time': user.update_time,
        'role': user.role,  # 0: 普通用户 1: 管理员
        'today_check_count': user.today_check_count(),
        'today_notification_count': user.today_notification_count(),
        'yesterday_check_count': user.yesterday_check_count(),
        'yesterday_notification_count': user.yesterday_notification_count(),
        'this_month_check_count': user.this_month_check_count(),
        'this_month_notification_count': user.this_month_notification_count(),
        'quota_exceeded': user.quota_exceeded,
        'invited': user.invitee_code is not None,
        'invitation_code': user.inviter_code,
    }
    return ok(data=ret)


# 用户修改自己信息
@user_bp.route('/user', methods=['PUT'])
@login_required
def update_user_info(user):
    nickname = request.form.get('nickname')
    email    = request.form.get('email')
    password = request.form.get('password')

    current_app.logger.info(f"user update info with user_id={user.id}, nickname={nickname}, email={email}")
        
    if not all([nickname, email, password]):
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    if len(nickname) < 2:
        return abort(ErrorCode.PARAMS_INVALID, msg="昵称长度不能小于2")
    if models.User.query.filter_by(email=email).first() and email != user.email:
        return abort(ErrorCode.USER_ALREADY_EXISTS, msg="邮箱已被使用")

    user.nickname = nickname
    user.email    = email
    user.password = password
    models.db.session.commit()
    return ok()


# 管理员获取所有用户信息
@user_bp.route('/users', methods=['GET'])
@login_required
def get_all_users_info(user):
    current_app.logger.info(f"admin get all users info with user_id={user.id}")

    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.User.query.filter_by(is_deleted=0).order_by(models.User.create_time.desc()))
    ret.items = [{
        'id': user.id,
        'email': user.email,
        'nickname': user.nickname,
        'create_time': user.create_time,
        'update_time': user.update_time,
        'role': user.role,
        'spaces': 1
    } for user in ret.items]
    # spaces里是用户的空间数量
    for user in ret.items:
        user['spaces'] = len(models.Space.query.filter_by(owner_id=user['id'], is_deleted=0).all())
    return ok(data=ret)


# 管理员获取某个用户信息
@user_bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_certain_user_info(user, user_id):
    current_app.logger.info(f"admin get certain user info with user_id={user.id}, target_user_id={user_id}")

    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    user = models.User.query.get(user_id)
    if not user:
        return abort(ErrorCode.NOT_FOUND)
    ret = {
        'id': user.id,
        'email': user.email,
        'nickname': user.nickname,
        'create_time': user.create_time,
        'update_time': user.update_time,
        'role': user.role, 
        'today_check_count': user.today_check_count(),
        'today_notification_count': user.today_notification_count(),
        'yesterday_check_count': user.yesterday_check_count(),
        'yesterday_notification_count': user.yesterday_notification_count(),
        'this_month_check_count': user.this_month_check_count(),
        'this_month_notification_count': user.this_month_notification_count(),
        'quota_exceeded': user.quota_exceeded,
        'invited': user.invitee_code is not None,
        'invitation_code': user.inviter_code,
    }
    return ok(data=ret)


# 管理员修改某个用户信息
@user_bp.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_certain_user_info(user, user_id):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    user = models.User.query.get(user_id)
    if not user:
        return abort(ErrorCode.NOT_FOUND)
    
    nickname = request.form.get('nickname')
    email    = request.form.get('email')
    password = request.form.get('password')
    role     = request.form.get('role')

    current_app.logger.info(f"admin update certain user info with user_id={user.id}, target_user_id={user_id}, nickname={nickname}, email={email}, role={role}")

    import re
    if email and not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        return abort(ErrorCode.PARAMS_INVALID, msg="邮箱格式错误")
    if nickname and len(nickname) < 2:
        return abort(ErrorCode.PARAMS_INVALID, msg="昵称长度不能小于2")
    if email and models.User.query.filter_by(email=email).first() and email != user.email:
        return abort(ErrorCode.USER_ALREADY_EXISTS, msg="邮箱已被使用")
    if role and int(role) not in [0, 1]:
        return abort(ErrorCode.PARAMS_INVALID, msg="角色参数错误")

    if nickname is not None:
        user.nickname = nickname
    if email is not None: 
        user.email = email
    if role is not None:     
        user.role = int(role)
    if password is not None: 
        user.password = password

    models.db.session.commit()
    return ok()


# 管理员软删除某个用户
@user_bp.route('/user/<int:user_id>/softdelete', methods=['PUT'])
@login_required
def softdelete_certain_user(user, user_id):
    current_app.logger.info(f"admin softdelete certain user with user_id={user.id}, target_user_id={user_id}")

    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    user = models.User.query.filter_by(id=user_id).first()
    if not user:
        return abort(ErrorCode.NOT_FOUND)
    
    user.is_deleted = 1
    # 软删除用户的所有空间、监视
    for space in user.spaces:
        for watch in space.watches:
            watch.is_deleted = 1
        space.is_deleted = 1
            
    models.db.session.commit()
    return ok()


# 管理员恢复某个用户
@user_bp.route('/user/<int:user_id>/restore', methods=['PUT'])
@login_required
def restore_certain_user(user, user_id):
    current_app.logger.info(f"admin restore certain user with user_id={user.id}, target_user_id={user_id}")

    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    user = models.User.query.filter_by(id=user_id).first()
    if not user:
        return abort(ErrorCode.NOT_FOUND)
    
    user.is_deleted = 0
    # 恢复用户的所有空间、监视
    for space in user.spaces:
        for watch in space.watches:
            watch.is_deleted = 0
        space.is_deleted = 0

    models.db.session.commit()
    return ok()


# 管理员硬删除某个用户
@user_bp.route('/user/<int:user_id>/delete', methods=['DELETE'])
@login_required
def delete_certain_user(user, user_id):
    current_app.logger.info(f"admin delete certain user with user_id={user.id}, target_user_id={user_id}")

    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    user = models.User.query.filter_by(id=user_id).first()
    if not user:
        return abort(ErrorCode.NOT_FOUND)
    
    # 删除用户的所有空间、监视
    for space in user.spaces:
        external_ids=[]
        for watch in space.watches:
            external_ids.append(watch.external_id)
            models.db.session.delete(watch)
        models.db.session.delete(space)
        models.db.session.commit()
        for id in external_ids:
            response = watch_utils.delete_watch(id)
    
    for check_count in user.check_counts:
        models.db.session.delete(check_count)

    models.db.session.delete(user)
    models.db.session.commit()
    return ok()


# 管理员增加某个用户 
@user_bp.route('/user', methods=['POST'])
@login_required
def add_user(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    
    email    = request.form.get('email')
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    role     = int(request.form.get('role'))

    current_app.logger.info(f"admin add user with user_id={user.id}, email={email}, nickname={nickname}, role={role}")

    if role not in [0, 1]:
        return abort(ErrorCode.PARAMS_INVALID, msg="角色参数错误")
    if not all([email, nickname, password]):
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        return abort(ErrorCode.PARAMS_INVALID, msg="邮箱格式错误")
    if len(nickname) < 2:
        return abort(ErrorCode.PARAMS_INVALID, msg="昵称长度不能小于2")
    if len(password) < 6:
        return abort(ErrorCode.PARAMS_INVALID, msg="密码长度不能小于6")
    if models.User.query.filter_by(email=email).first():
        return abort(ErrorCode.USER_ALREADY_EXISTS, msg="邮箱已被使用")
    
    user = models.User(email=email, nickname=nickname, password=password, role=role)
    
    # 激活用户
    user.activated = True
    user.activated_on = models.datetime.now()

    models.db.session.add(user)
    models.db.session.commit()

    user = models.User.query.filter_by(email=email).first()
    # 创建默认空间
    space = models.Space(name=f'默认空间', desc=f'用户{user.email}的默认空间', owner_id=user.id)
    models.db.session.add(space)

    models.db.session.commit()

    return ok()


# 管理员根据email和nickname搜索用户
@user_bp.route('/users/search', methods=['GET'])
@login_required
def search_user(user):
    email    = request.args.get('email')
    nickname = request.args.get('nickname')

    current_app.logger.info(f"admin search user with user_id={user.id}, email={email}, nickname={nickname}")

    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)

    if not any([email, nickname]):
        ret = paginate(models.User.query.filter_by(is_deleted=0).order_by(models.User.create_time.desc()))
    else:
        if email:
            if nickname:
                ret = paginate(models.User.query.filter(models.User.email.like(f'%{email}%'), models.User.nickname.like(f'%{nickname}%'), models.User.is_deleted==0).order_by(models.User.create_time.desc()))
            else:
                ret = paginate(models.User.query.filter(models.User.email.like(f'%{email}%'), models.User.is_deleted==0).order_by(models.User.create_time.desc()))
        else:   
            ret = paginate(models.User.query.filter(models.User.nickname.like(f'%{nickname}%'), models.User.is_deleted==0).order_by(models.User.create_time.desc()))
    ret.items = [{
        'id': user.id,
        'email': user.email,
        'nickname': user.nickname,
        'create_time': user.create_time,
        'update_time': user.update_time,
        'role': user.role,  # 0: 普通用户 1: 管理员
        'spaces': 1
    } for user in ret.items]
    # spaces里是用户的空间数量
    for user in ret.items:
        user['spaces'] = len(models.Space.query.filter_by(owner_id=user['id'], is_deleted = 0).all())
    return ok(data=ret)
    
    
# 管理员获取所有软删除的用户
@user_bp.route('/users/softdelete', methods=['GET'])
@login_required
def get_users_softdeleted(user):
    current_app.logger.info(f"admin get softdeleted users with user_id={user.id}")

    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.User.query.filter_by(is_deleted=1).order_by(models.User.create_time.desc()))
    ret.items = [{
        'id': user.id,
        'email': user.email,
        'nickname': user.nickname,
        'create_time': user.create_time,
        'update_time': user.update_time,
        'role': user.role,
        'spaces': 1
    } for user in ret.items]
    # spaces里是用户的空间数量
    for user in ret.items:
        user['spaces'] = len(models.Space.query.filter_by(owner_id=user['id']).all())
    return ok(data=ret)


# 用户获取自己邀请列表（分页）
@user_bp.route('/user/invitations', methods=['GET'])
@login_required
def get_invitation_list(user):
    current_app.logger.info(f"user get invitations with user_id={user.id}")
    ret = paginate(models.UserInvitation.query.filter_by(inviter_id=user.id) \
                   .order_by(models.UserInvitation.create_time.desc()))
    ret.items = [{
        'email': invitation.invitee_email,
        'create_time': invitation.create_time,
    } for invitation in ret.items]
    return ok(data=ret)


# 用户刷新邀请码
@user_bp.route('/user/invitation_code', methods=['PUT'])
@login_required
def refresh_invitation_code(user):
    current_app.logger.info(f"user refresh invitation code with user_id={user.id}")
    user.inviter_code = generate_invitation_code()
    models.db.session.commit()
    return ok(data={
        'invitation_code': user.inviter_code
    })


# 用户使用邀请码
@user_bp.route('/user/invitation_code', methods=['POST'])
@login_required
def use_invitation_code(user):
    code = request.form.get('invitation_code')
    current_app.logger.info(f"user use invitation code with user_id={user.id}, code={code}")

    if not code:
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    if user.invitee_code is not None:
        return abort(ErrorCode.HAVE_BEEN_INVITED)

    inviter = models.User.query.filter_by(inviter_code=code, is_deleted=0).first()
    if inviter.id == user.id:
        return abort(ErrorCode.CANNOT_INVIT_SELF)
    if not inviter: 
        return abort(ErrorCode.INVITATION_CODE_INVALID)
    
    user.invitee_code = code
    
    invitation = models.UserInvitation(inviter_id=inviter.id, invitee_id=user.id, invitee_email=user.email)
    models.db.session.add(invitation)
    models.db.session.commit()

    add_invitation_bonus(inviter, user)
    return ok()

