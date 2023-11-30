from webmonitor.user import user_bp
from webmonitor import models
from flask import render_template, request
from flask_restful import Resource
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email
from webmonitor.utils.auth import login_required
import webmonitor.utils.watch as watch_utils
from webmonitor.utils.page import paginate


# 用户获取自己信息
@user_bp.route('/user', methods=['GET'])
@login_required
def get_user_info(user):
    ret = {
        'id': user.id,
        'email': user.email,
        'nickname': user.nickname,
        'create_time': user.create_time,
        'update_time': user.update_time,
        'role': user.role,  # 0: 普通用户 1: 管理员
        'spaces': []
    }
    for space in user.spaces:
        ret['spaces'].append({
            'id': space.id,
            'name': space.name,
            'desc': space.desc,
            'create_time': space.create_time,
            'update_time': space.update_time,
        })
    return ok(data=ret)


# 用户修改自己信息
@user_bp.route('/user', methods=['PUT'])
@login_required
def update_user_info(user):
    nickname = request.form.get('nickname')
    email    = request.form.get('email')
    password = request.form.get('password')
    if not all([nickname, email, password]):
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    if len(nickname) < 2:
        return abort(ErrorCode.PARAMS_INVALID, msg="昵称长度不能小于2")
    user.nickname = nickname
    user.email    = email
    user.password = password
    models.db.session.commit()
    return ok()

# 管理员获取所有用户信息
@user_bp.route('/users', methods=['GET'])
@login_required
def get_all_users_info(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.User.query)
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

# 管理员获取某个用户信息
@user_bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_certain_user_info(user, user_id):
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
        'spaces': []
    }
    # spaces = models.Space.query.filter_by(owner_id=user.id).all()
    for space in user.spaces:
        ret['spaces'].append({
            'id': space.id,
            'name': space.name,
            'desc': space.desc,
            'create_time': space.create_time,
            'update_time': space.update_time,
        })
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
    if not all([nickname, email]):
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        return abort(ErrorCode.PARAMS_INVALID, msg="邮箱格式错误")
    if len(nickname) < 2:
        return abort(ErrorCode.PARAMS_INVALID, msg="昵称长度不能小于2")
    user.nickname = nickname
    user.email    = email
    if password is not None:
        user.password = password
    models.db.session.commit()
    return ok()

# 管理员软删除某个用户
@user_bp.route('/user/<int:user_id>/softdelete', methods=['PUT'])
@login_required
def softdelete_certain_user(user, user_id):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    user = models.User.query.filter_by(id=user_id).first()
    if not user:
        return abort(ErrorCode.NOT_FOUND)
    
    user.is_deleted = 1
    models.db.session.commit()
    return ok()

# 管理员恢复某个用户
@user_bp.route('/user/<int:user_id>/restore', methods=['PUT'])
@login_required
def restore_certain_user(user, user_id):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    user = models.User.query.filter_by(id=user_id).first()
    if not user:
        return abort(ErrorCode.NOT_FOUND)
    
    user.is_deleted = 0
    models.db.session.commit()
    return ok()

# 管理员硬删除某个用户
@user_bp.route('/user/<int:user_id>/delete', methods=['DELETE'])
@login_required
def delete_certain_user(user, user_id):
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
        return abort(ErrorCode.USER_ALREADY_EXISTS, msg="用户已存在")
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
@user_bp.route('/user/search', methods=['GET'])
@login_required
def search_user(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    email    = request.form.get('email')
    nickname = request.form.get('nickname')
    if not any([email, nickname]):
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    
    if email:
        if nickname:
            ret = paginate(models.User.query.filter(models.User.email.like(f'%{email}%'), models.User.nickname.like(f'%{nickname}%')))
        else:
            ret = paginate(models.User.query.filter(models.User.email.like(f'%{email}%')))
    else:
        ret = paginate(models.User.query.filter(models.User.nickname.like(f'%{nickname}%')))

    ret.items = [{
        'id': user.id,
        'email': user.email,
        'nickname': user.nickname,
        'create_time': user.create_time,
        'update_time': user.update_time,
        'spaces': 1
    } for user in ret.items]
    # spaces里是用户的空间数量
    for user in ret.items:
        user['spaces'] = len(models.Space.query.filter_by(owner_id=user['id']).all())
    
    return ok(data=ret)
    
    
    