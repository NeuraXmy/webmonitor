from webmonitor.space import space_bp
from webmonitor import models
from flask import render_template, request
from flask_restful import Resource
from webmonitor.utils.response import make_response
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email
from webmonitor.utils.auth import login_required


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


