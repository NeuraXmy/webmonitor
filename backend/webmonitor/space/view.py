from webmonitor.space import space_bp
from webmonitor import models
from flask import render_template, request
from flask_restful import Resource
from webmonitor.utils.response import make_response
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email
from webmonitor.utils.auth import login_required
import webmonitor.utils.watch as watch_utils


# 用户获取自己空间列表
@space_bp.route('/spaces', methods=['GET'])
@login_required
def get_space_list(user):
    ret_spaces = []
    for space in user.spaces:
        ret_spaces.append({
            'id': space.id,
            'name': space.name,
            'create_time': space.create_time,
            'update_time': space.update_time,
        })
    return make_response(200, data=ret_spaces)


# 用户获取某个空间详细信息
@space_bp.route('/space/<int:space_id>', methods=['GET'])
@login_required
def get_space(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return make_response(404, msg="空间不存在")
    if space.owner_id != user.id:
        return make_response(403, msg="无权访问")
    
    ret = {
        'id': space.id,
        'name': space.name,
        'desc': space.desc,
        'create_time': space.create_time,
        'update_time': space.update_time,
    }

    return make_response(200, data=ret)


# 用户创建空间
@space_bp.route('/space', methods=['POST'])
@login_required
def create_space(user):
    name = request.form.get('name')
    desc = request.form.get('desc')
    if not name:
        return make_response(400, msg="空间名不能为空")
    if len(name) > 20:
        return make_response(400, msg="空间名不能超过20个字符")
    if desc and len(desc) > 512:
        return make_response(400, msg="空间描述不能超过512个字符")

    space = models.Space(name=name, desc=desc, owner_id=user.id)
    models.db.session.add(space)
    models.db.session.commit()

    return make_response(200)
    

# 用户修改空间
@space_bp.route('/space/<int:space_id>', methods=['PUT'])
@login_required
def modify_space(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return make_response(404, msg="空间不存在")
    if space.owner_id != user.id:
        return make_response(403, msg="无权访问")

    name = request.form.get('name')
    desc = request.form.get('desc')
    if not name:
        return make_response(400, msg="空间名不能为空")
    if len(name) > 20:
        return make_response(400, msg="空间名不能超过20个字符")
    if desc and len(desc) > 512:
        return make_response(400, msg="空间描述不能超过512个字符")

    space.name = name
    space.desc = desc
    models.db.session.commit()

    return make_response(200)


# 用户删除空间
@space_bp.route('/space/<int:space_id>', methods=['DELETE'])
@login_required
def delete_space(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return make_response(404, msg="空间不存在")
    if space.owner_id != user.id:
        return make_response(403, msg="无权访问")
    
    # 先尝试删除空间下的所有监控，如果数据库操作成功，再从changedetection.io删除watch
    external_ids = []
    for watch in space.watches:
        external_ids.append(watch.external_id)
        models.db.session.delete(watch)
    models.db.session.delete(space)
    models.db.session.commit()
    for id in external_ids:
        response = watch_utils.delete_watch(id)
        
    return make_response(200)


