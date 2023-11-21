from webmonitor.bookmark import bookmark_bp
from flask import send_file, current_app, request
from webmonitor.utils.auth import login_required
from webmonitor.utils.response import make_response

@bookmark_bp.route('/bookmark/inject.js', methods=['GET'])
@login_required
def get_inject(user):
    token = request.headers['token']
    with open('webmonitor/static/inject.js', 'r', encoding='utf-8') as f:
        js_file = f.read()
    js_file = js_file.replace('####token####', token).replace('####base_url####', current_app.config['FRONTEND_BASE_URL'])
    return make_response(200, data=js_file)