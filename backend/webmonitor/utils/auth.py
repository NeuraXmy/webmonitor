from webmonitor.models import User
from webmonitor.utils.token import verify_token
from webmonitor.utils.response import make_response
from functools import wraps
from flask import request, redirect, url_for


# 验证用户登录装饰器
def login_required(view_func):
    @wraps(view_func)
    def decorated_func(*args, **kwargs):
        try:
            token = request.headers['token']
        except Exception:
            return make_response(401, msg="缺少验证token")
        
        try:
            user_id = verify_token(token, 7 * 24 * 3600)
        except Exception:
            return make_response(401, msg="token无效")
        
        user = User.query.get(user_id)
        if not user:
            return make_response(401, msg="用户不存在")
        if not user.activated:
            return make_response(401, msg="用户未激活")
        
        return view_func(user, *args, **kwargs)
    return decorated_func