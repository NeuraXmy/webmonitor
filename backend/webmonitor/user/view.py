from webmonitor.user import user_bp
from webmonitor import models
from flask import render_template, request
from flask_restful import Resource
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email
from webmonitor.utils.auth import login_required


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
    if not nickname:
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    if len(nickname) < 2:
        return abort(ErrorCode.PARAMS_INVALID, msg="昵称长度不能小于2")
    user.nickname = nickname
    models.db.session.commit()
    return ok()