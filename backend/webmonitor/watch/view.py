from webmonitor.watch import watch_bp
from webmonitor import models
from flask import render_template, request
from flask_restful import Resource
from webmonitor.utils.response import make_response
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email
from webmonitor.utils.auth import login_required
import webmonitor.utils.watch as watch_utils


# 用户获取某个监控详细信息
@watch_bp.route('/watch/<int:watch_id>', methods=['GET'])
@login_required
def get_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    space = models.Space.query.get(watch.space_id)
    if not watch:
        return make_response(404, msg="监控不存在")
    if space.owner_id != user.id:
        return make_response(403, msg="无权访问")
    ret = {
        'id': watch.id,
        'name': watch.name,
        'desc': watch.desc,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'time_between_check_weeks': watch.time_between_check_weeks,
        'time_between_check_days': watch.time_between_check_days,
        'time_between_check_hours': watch.time_between_check_hours,
        'time_between_check_minutes': watch.time_between_check_minutes,
        'time_between_check_seconds': watch.time_between_check_seconds,
        'notification_email': watch.notification_email,
    }
    return make_response(200, data=ret)


# 用户在某个空间下创建监控
@watch_bp.route('/space/<int:space_id>/watch', methods=['POST'])
@login_required
def create_watch(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return make_response(404, msg="空间不存在")
    if space.owner_id != user.id:
        return make_response(403, msg="无权访问")
    
    watch = models.Watch()
    watch.name = request.form.get('name')
    watch.desc = request.form.get('desc')
    
    watch.url = request.form.get('url')
    if not watch.url:
        return make_response(400, msg="参数不完整")
    
    watch.space_id = space_id
    watch.time_between_check_weeks = request.form.get('time_between_check_weeks')
    watch.time_between_check_days = request.form.get('time_between_check_days')
    watch.time_between_check_hours = request.form.get('time_between_check_hours')
    watch.time_between_check_minutes = request.form.get('time_between_check_minutes')
    watch.time_between_check_seconds = request.form.get('time_between_check_seconds')
    watch.notification_email = request.form.get('notification_email')
    
    # 在changedetection.io上创建监控
    watch.external_id = watch_utils.create_watch(watch.url)
    
    models.db.session.add(watch)
    models.db.session.commit()

    return make_response(200)


# 用户获取某个空间的监控列表
@watch_bp.route('/space/<int:space_id>/watches', methods=['GET'])
@login_required
def get_watch_list(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return make_response(404, msg="空间不存在")
    if space.owner_id != user.id:
        return make_response(403, msg="无权访问")
    
    ret_watches = []
    for watch in space.watches:
        ret_watches.append({
            'id': watch.id,
            'name': watch.name,
            'url': watch.url,
            'create_time': watch.create_time,
            'update_time': watch.update_time,
            'last_check_time': watch.last_check_time,
        })
    return make_response(200, data=ret_watches)


# 用户删除监控
@watch_bp.route('/watch/<int:watch_id>', methods=['DELETE'])
@login_required
def delete_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    if not watch:
        return make_response(404, msg="监控不存在")
    space = models.Space.query.get(watch.space_id)
    if space.owner_id != user.id:
        return make_response(403, msg="无权访问")
    
    # 在changedetection.io上删除监控
    watch_utils.delete_watch(watch.external_id)

    models.db.session.delete(watch)
    models.db.session.commit()

    return make_response(200)


# 用户修改监控
@watch_bp.route('/watch/<int:watch_id>', methods=['PUT'])
@login_required
def update_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    if not watch:
        return make_response(404, msg="监控不存在")
    space = models.Space.query.get(watch.space_id)
    if space.owner_id != user.id:
        return make_response(403, msg="无权访问")

    update_data = {}
    # url必须有且不为空
    url = request.form.get('url')
    update_data["url"] = url
    watch.url = url


    if request.form.get('name'):
        watch.name = request.form.get('name')
    if request.form.get('desc'):
        watch.desc = request.form.get('desc')
    if request.form.get('notification_email'):
        watch.notification_email = request.form.get('notification_email')


    if request.form.get('time_between_check_weeks'):
        watch.time_between_check_weeks = int(request.form.get('time_between_check_weeks'))
        update_data["time_between_check_weeks"] = watch.time_between_check_weeks
    if request.form.get('time_between_check_days'):
        watch.time_between_check_days = int(request.form.get('time_between_check_days'))
        update_data["time_between_check_days"] = watch.time_between_check_days
    if request.form.get('time_between_check_hours'):
        watch.time_between_check_hours = int(request.form.get('time_between_check_hours'))
        update_data["time_between_check_hours"] = watch.time_between_check_hours
    if request.form.get('time_between_check_minutes'):
        watch.time_between_check_minutes = int(request.form.get('time_between_check_minutes'))
        update_data["time_between_check_minutes"] = watch.time_between_check_minutes
    if request.form.get('time_between_check_seconds'):
        watch.time_between_check_seconds = int(request.form.get('time_between_check_seconds'))
        update_data["time_between_check_seconds"] = watch.time_between_check_seconds

    # 包含部分，支持xpath,jsonpath,css选择器
    if request.form.get('include_filters'):
        include_filters = request.form.get('include_filters')
        include_filters = include_filters.split('\n')
        update_data["include_filters"] = include_filters

    # 去除部分,如header,footer,nav等
    if request.form.get('subtractive_selectors'):
        subtractive_selectors = request.form.get('subtractive_selectors')
        subtractive_selectors = subtractive_selectors.split('\n')
        update_data["subtractive_selectors"] = subtractive_selectors

    # 触发部分，有就提醒，支持正则表达式
    if request.form.get('trigger_text'):
        trigger_text = request.form.get('trigger_text')
        trigger_text = trigger_text.split('\n')
        update_data["trigger_text"] = trigger_text

    # 忽略部分，支持正则表达式
    if request.form.get('ignore_text'):
        ignore_text = request.form.get('ignore_text')
        ignore_text = ignore_text.split('\n')
        update_data["ignore_text"] = ignore_text


    watch_utils.update_watch(watch.external_id, update_data)
    
    models.db.session.commit()
    return make_response(200)


# 用户立刻刷新监控
@watch_bp.route('/watch/<int:watch_id>/check', methods=['POST'])
@login_required
def check_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    if not watch:
        return make_response(404, msg="监控不存在")
    space = models.Space.query.get(watch.space_id)
    if space.owner_id != user.id:
        return make_response(403, msg="无权访问")
    
    # 查询最近一次快照
    last_snapshot = watch_utils.get_latest_snapshot(watch.external_id)
    
    # 在changedetection.io上立刻刷新监控
    watch_utils.update_watch_state(watch.external_id, recheck=True)

    # 延迟等待changedetection.io刷新监控
    import time
    time.sleep(5)

    # 查询历史进行比对，如果有变更则发送邮件
    snapshot = watch_utils.get_latest_snapshot(watch.external_id)
    if snapshot != last_snapshot:
        import difflib
        diff = difflib.HtmlDiff().make_file(last_snapshot.splitlines(), snapshot.splitlines())
        # 发送邮件通知
        if watch.notification_email:
            send_email(watch.notification_email, 
                    'webmonitor-监控项变更通知', 
                    'email/notification.html', 
                    watch=watch, diff=diff)
        
    # 更新监控的最后检查时间
    watch.last_check_time = models.datetime.now()
    models.db.session.commit()

    return make_response(200)

