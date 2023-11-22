from webmonitor.models import User
from webmonitor.utils.token import verify_token
from webmonitor.utils.error import ErrorCode, abort
from functools import wraps
from flask import request, redirect, url_for


# 验证用户登录装饰器
def login_required(view_func):
    @wraps(view_func)
    def decorated_func(*args, **kwargs):
        try:
            token = request.headers['token']
        except Exception:
            return abort(ErrorCode.TOKEN_INVALID, msg="缺少身份认证token")
    
        try:
            user_id = verify_token(token, 7 * 24 * 3600)
        except Exception:
            return abort(ErrorCode.TOKEN_INVALID, msg="身份认证token无效")
        
        user = User.query.get(user_id)
        if not user:
            return abort(ErrorCode.USER_NOT_FOUND)
        if not user.activated:
            return abort(ErrorCode.USER_NOT_ACTIVATED)
        
        return view_func(user, *args, **kwargs)
    return decorated_func