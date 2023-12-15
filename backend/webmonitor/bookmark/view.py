from webmonitor.bookmark import bookmark_bp
from flask import send_file, current_app, request
from webmonitor.utils.auth import login_required
from webmonitor.utils.error import ok


# 返回书签注入脚本
@bookmark_bp.route('/bookmark/inject.js', methods=['GET'])
@login_required
def get_inject(user):
    token = request.headers['token']

    current_app.logger.info(f"inject.js requested with user_id={user.id}")

    with open('webmonitor/static/inject.js', 'r', encoding='utf-8') as f:
        js_file = f.read()
    js_file = js_file.replace('####token####', token).replace('####base_url####', current_app.config['FRONTEND_BASE_URL'])
    return ok(data=js_file)