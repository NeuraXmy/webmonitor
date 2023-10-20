status_msg = {
    200: 'OK',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    408: 'Request Timeout',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
}

def make_response(status, data=None, msg=None):
    if status in status_msg and msg is None:
        msg = status_msg[status]
    if data is None:
        return {'status': status, 'msg': msg}
    return {'status': status, 'msg': msg, 'data': data}