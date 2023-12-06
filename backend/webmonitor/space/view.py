from webmonitor.space import space_bp
from webmonitor import models
from flask import render_template, request
from flask_restful import Resource
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email
from webmonitor.utils.auth import login_required
import webmonitor.utils.watch as watch_utils
from webmonitor.utils.page import paginate


# 用户获取自己空间列表
@space_bp.route('/spaces', methods=['GET'])
@login_required
def get_space_list(user):
    ret = models.Space.query.filter_by(owner_id=user.id, is_deleted=0).order_by(models.Space.create_time).all()
    ret = { 
        'items': [{
            'id': space.id,
            'name': space.name,
            'create_time': space.create_time,
            'update_time': space.update_time,
        } for space in ret]
    }
    return ok(data=ret)


# 管理员使用，获取某个用户的空间列表
@space_bp.route('/user/<int:user_id>/spaces', methods=['GET'])
@login_required
def get_space_list_by_user(user, user_id):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.Space.query.filter_by(owner_id=user_id, is_deleted=0).order_by(models.Space.create_time.desc()))
    ret.items = [{
        'id': space.id,
        'name': space.name,
        'create_time': space.create_time,
        'update_time': space.update_time,
    } for space in ret.items]
    return ok(data=ret)


# 用户获取某个空间详细信息
@space_bp.route('/space/<int:space_id>', methods=['GET'])
@login_required
def get_space(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return abort(ErrorCode.NOT_FOUND)
    if user.role != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    return ok(data={
        'id': space.id,
        'name': space.name,
        'desc': space.desc,
        'create_time': space.create_time,
        'update_time': space.update_time,
    })


# 用户创建空间
@space_bp.route('/space', methods=['POST'])
@login_required
def create_space(user):
    name = request.form.get('name')
    desc = request.form.get('desc')
    if not name:
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    if len(name) > 20:
        return abort(ErrorCode.PARAMS_INVALID, msg="空间名不能超过20个字符")
    if desc and len(desc) > 512:
        return abort(ErrorCode.PARAMS_INVALID, msg="空间描述不能超过512个字符")

    space = models.Space(name=name, desc=desc, owner_id=user.id)
    models.db.session.add(space)
    models.db.session.commit()
    return ok()
    

# 管理员给一个用户创建空间
@space_bp.route('/user/<int:user_id>/space', methods=['POST'])
@login_required
def create_space_by_user(user, user_id):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    name = request.form.get('name')
    desc = request.form.get('desc')
    if not name:
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    if len(name) > 20:
        return abort(ErrorCode.PARAMS_INVALID, msg="空间名不能超过20个字符")
    if desc and len(desc) > 512:
        return abort(ErrorCode.PARAMS_INVALID, msg="空间描述不能超过512个字符")

    space = models.Space(name=name, desc=desc, owner_id=user_id)
    models.db.session.add(space)
    models.db.session.commit()
    return ok()


# 用户修改空间
@space_bp.route('/space/<int:space_id>', methods=['PUT'])
@login_required
def modify_space(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return abort(ErrorCode.NOT_FOUND)
    if user.role != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)

    name = request.form.get('name')
    desc = request.form.get('desc')
    if not name:
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    if len(name) > 20:
        return abort(ErrorCode.PARAMS_INVALID, msg="空间名不能超过20个字符")
    if desc and len(desc) > 512:
        return abort(ErrorCode.PARAMS_INVALID, msg="空间描述不能超过512个字符")

    space.name = name
    space.desc = desc
    models.db.session.commit()
    return ok()


# 用户删除空间
@space_bp.route('/space/<int:space_id>', methods=['DELETE'])
@login_required
def delete_space(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return abort(ErrorCode.NOT_FOUND)
    if user.role != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    # 先尝试删除空间下的所有监控，如果数据库操作成功，再从changedetection.io删除watch
    external_ids = []
    for watch in space.watches:
        external_ids.append(watch.external_id)
        models.db.session.delete(watch)
    models.db.session.delete(space)
    models.db.session.commit()
    for id in external_ids:
        response = watch_utils.delete_watch(id)
    return ok()


# 管理员根据name搜索空间
@space_bp.route('/spaces/search', methods=['GET'])
@login_required
def search_spaces(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    name = request.args.get('name')
    if not name:
        ret = paginate(models.Space.query.filter_by(is_deleted=0).order_by(models.Space.create_time.desc()))
    else:
        ret = paginate(models.Space.query.filter(models.Space.name.like(f'%{name}%'), models.Space.is_deleted==0).order_by(models.Space.create_time.desc()))
    
    ret.items = [{
        'id': space.id,
        'name': space.name,
        'desc': space.desc,
        'create_time': space.create_time,
        'update_time': space.update_time,
        'owner_id': space.owner_id,
        'owner_email': ''
    } for space in ret.items]
    for space in ret.items:
        space['owner_email'] = models.User.query.get(space['owner_id']).email
    # 删除owner_id字段
    for space in ret.items:
        del space['owner_id']
    return ok(data=ret)
    

# 管理员获取所有空间列表
@space_bp.route('/spaces/all', methods=['GET'])
@login_required
def get_all_spaces(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.Space.query.filter_by(is_deleted=0).order_by(models.Space.create_time.desc()))
    ret.items = [{
        'id': space.id,
        'name': space.name,
        'desc': space.desc,
        'create_time': space.create_time,
        'update_time': space.update_time,
        'owner_id': space.owner_id,
        'owner_email':''
    } for space in ret.items]
    for space in ret.items:
        space['owner_email'] = models.User.query.get(space['owner_id']).email
    # 删除owner_id字段
    for space in ret.items:
        del space['owner_id']
    return ok(data=ret)


# 管理员软删除空间
@space_bp.route('/space/<int:space_id>/softdelete', methods=['PUT'])
@login_required
def soft_delete_space(user, space_id):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    space = models.Space.query.filter_by(id=space_id).first()
    if not space:
        return abort(ErrorCode.NOT_FOUND)
    space.is_deleted = 1
    for watch in space.watches:
        watch.is_deleted = 1
    models.db.session.commit()
    return ok()


# 管理员恢复软删除的空间
@space_bp.route('/space/<int:space_id>/restore', methods=['PUT'])
@login_required
def restore_space(user, space_id):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    space = models.Space.query.filter_by(id=space_id).first()
    if not space:
        return abort(ErrorCode.NOT_FOUND)
    owner = models.User.query.get(space.owner_id)
    if owner.is_deleted == 1:
        return abort(ErrorCode.SAPCE_RESTORE_FAIL)
    space.is_deleted = 0
    for watch in space.watches:
        watch.is_deleted = 0
    models.db.session.commit()
    return ok()


# 管理员获取软删除的空间列表
@space_bp.route('/spaces/softdelete', methods=['GET'])
@login_required
def get_spaces_softdeleted(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.Space.query.filter_by(is_deleted=1).order_by(models.Space.update_time.desc()))
    ret.items = [{
        'id': space.id,
        'name': space.name,
        'desc': space.desc,
        'create_time': space.create_time,
        'update_time': space.update_time,
        'owner_id': space.owner_id,
        'owner_email': ''
    } for space in ret.items]
    
    i=0
    while(i<len(ret.items)):
        owner = models.User.query.get(ret.items[i]['owner_id'])
        ret.items[i]['owner_email'] = owner.email
        if owner.is_deleted == 1:
            ret.items.remove(ret.items[i])
        else:
            i+=1
    # 删除owner_id字段
    for space in ret.items:
        del space['owner_id']
    return ok(data=ret)