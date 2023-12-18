from flask import make_response, current_app
from enum import Enum


class ErrorCode(Enum):
    # ---------------------- 通用错误   ---------------------- #
    OK                    = (200, 200, "成功")   
    INTERNAL_SERVER_ERROR = (500, 500, "内部服务器错误")
    PARAMS_INVALID        = (400, 400, "参数无效")
    PARAMS_INCOMPLETE     = (400, 400, "参数不完整")
    NOT_FOUND             = (404, 404, "资源不存在")
    FORBIDDEN             = (403, 403, "无访问权限")

    # ---------------------- 6xx misc  ---------------------- #
    EMAIL_SEND_FAIL       = (200, 600, "邮件发送失败")

    # ---------------------- 7xx auth  ---------------------- #
    USER_ALREADY_ACTIVATED = (200, 700, "用户已激活")
    USER_NOT_ACTIVATED     = (200, 701, "用户未激活")
    TOKEN_INVALID          = (200, 702, "身份认证token无效")
    USER_NOT_FOUND         = (200, 703, "用户不存在")
    PASSWORD_ERROR         = (200, 704, "密码错误")
    USER_ALREADY_EXISTS    = (200, 705, "用户已存在")
    
    # ---------------------- 8xx watch ---------------------- #
    WATCH_RESTORE_FAIL     = (200, 800, "空间被软删除，无法恢复监控项")
    WATCH_ALREADY_PAUSED   = (200, 801, "监控项已暂停")
    USER_QUOTA_EXCEEDED    = (200, 802, "用户配额超出限制")
    SPACE_QUOTA_EXCEEDED   = (200, 803, "空间配额超出限制")

    # ---------------------- 9xx space ---------------------- #
    SAPCE_RESTORE_FAIL           = (200, 900, "用户被软删除，无法恢复空间")

    # ---------------------- 10xx user ---------------------- #

    def __init__(self, http_status, code, msg) -> None:
        self.http_status = http_status   # HTTP状态码 
        self.code = code                 # 后端错误码
        self.msg = msg                   # 错误消息

    def to_response(self, msg=None, data=None):
        # 因为不方便修改，返回前端时错误码仍然命名为status而不是code
        if data:
            response = make_response({
                "status": self.code,  
                "msg": msg,
                "data": data
            }, self.http_status)
        else:
            response = make_response({
                "status": self.code,
                "msg": msg
            }, self.http_status)
        response.headers["Content-Type"] = "application/json"
        return response


class APIException(Exception):
    def __init__(self, error_code: ErrorCode, msg=None):
        self.error_code = error_code
        self.msg = msg
        super().__init__(error_code.msg)
    

def abort(error_code: ErrorCode, msg=None):
    if not msg:
        msg = error_code.msg
    current_app.logger.info(f"response sent with error_code={error_code.code}, msg={msg}")
    raise APIException(error_code, msg)

def ok(msg=None, data=None):
    if not msg:
        msg = ErrorCode.OK.msg
    current_app.logger.info(f"response sent with error_code={ErrorCode.OK.code}, msg={msg}")
    return ErrorCode.OK.to_response(msg, data)
    

