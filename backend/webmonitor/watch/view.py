from webmonitor.watch import watch_bp
from webmonitor import models
from flask import render_template, request
from flask_restful import Resource
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email
from webmonitor.utils.auth import login_required
import webmonitor.utils.watch as watch_utils
from webmonitor.utils.page import paginate


# 用户获取某个监控详细信息
@watch_bp.route('/watch/<int:watch_id>', methods=['GET'])
@login_required
def get_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    space = models.Space.query.get(watch.space_id)
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    # manager or owner
    if user.id != 1 and space.owner_id != user.id: 
        return abort(ErrorCode.FORBIDDEN)
    ret = {
        'id': watch.id,
        'name': watch.name,
        'desc': watch.desc,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_state,
        'time_between_check_weeks': watch.time_between_check_weeks,
        'time_between_check_days': watch.time_between_check_days,
        'time_between_check_hours': watch.time_between_check_hours,
        'time_between_check_minutes': watch.time_between_check_minutes,
        'time_between_check_seconds': watch.time_between_check_seconds,
        'include_filters': watch.include_filters,
        'trigger_text': watch.trigger_text,
        'notification_email': watch.notification_email,
    }
    return ok(data=ret)


# 用户在某个空间下创建监控
@watch_bp.route('/space/<int:space_id>/watch', methods=['POST'])
@login_required
def create_watch(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return abort(ErrorCode.NOT_FOUND)
    if user.id !=1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    watch = models.Watch()

    # 获取watch数据
    watch.name = request.form.get('name')
    watch.desc = request.form.get('desc')
    
    watch.url = request.form.get('url')
    if not watch.url:
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    if not watch.url.startswith('http://') and not watch.url.startswith('https://'):
        return abort(ErrorCode.PARAMS_INVALID, msg="url不合法")
    
    watch.space_id = space_id
    for unit in ['weeks', 'days', 'hours', 'minutes', 'seconds']:
        setattr(watch, f'time_between_check_{unit}', int(request.form.get(f'time_between_check_{unit}')))
    watch.notification_email    = request.form.get('notification_email')
    watch.include_filters       = request.form.get('include_filters')
    watch.trigger_text          = request.form.get('trigger_text')
    
    # 在changedetection.io上创建监控
    external_id = watch_utils.create_watch(watch)
    watch.external_id = external_id

    # 保存监控到数据库
    models.db.session.add(watch)
    models.db.session.commit()
    
    # 创建成功，在cdio上更新监控id（这里是因为在保存到数据库之前不知道监控id）
    watch_utils.update_watch(external_id, watch)
    # TODO 如果创建失败需要删除changedetection.io上的监控

    return ok()


# 用户获取某个空间的监控列表
@watch_bp.route('/space/<int:space_id>/watches', methods=['GET'])
@login_required
def get_watch_list(user, space_id):
    space = models.Space.query.get(space_id)
    if not space:
        return abort(ErrorCode.NOT_FOUND)
    if user.id != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    # 获取监控列表
    ret = paginate(models.Watch.query.filter_by(space_id=space_id))
    ret.items = [{
        'id': watch.id,
        'name': watch.name,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_state,
    } for watch in ret.items]
    return ok(data=ret)


# 用户删除监控
@watch_bp.route('/watch/<int:watch_id>', methods=['DELETE'])
@login_required
def delete_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    space = models.Space.query.get(watch.space_id)
    if user.id != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    external_id = watch.external_id
    models.db.session.delete(watch)
    models.db.session.commit()

    # 如果数据库更新成功，在changedetection.io上删除监控
    response = watch_utils.delete_watch(external_id)
    return ok()


# 用户修改监控
@watch_bp.route('/watch/<int:watch_id>', methods=['PUT'])
@login_required
def update_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    space = models.Space.query.get(watch.space_id)
    if user.id != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)

    # 获取watch数据
    watch.name = request.form.get('name')
    watch.desc = request.form.get('desc')
    
    watch.url = request.form.get('url')
    if not watch.url:
        return abort(ErrorCode.PARAMS_INCOMPLETE)
    if not watch.url.startswith('http://') and not watch.url.startswith('https://'):
        return abort(ErrorCode.PARAMS_INVALID, msg="url不合法")
    
    for unit in ['weeks', 'days', 'hours', 'minutes', 'seconds']:
        setattr(watch, f'time_between_check_{unit}', int(request.form.get(f'time_between_check_{unit}')))
    watch.notification_email    = request.form.get('notification_email')
    watch.include_filters       = request.form.get('include_filters')
    watch.trigger_text          = request.form.get('trigger_text')

    # 更新数据到cdio
    watch_utils.update_watch(watch.external_id, watch)

    # 更新到数据库
    models.db.session.commit()
    return ok()


# 用户立刻刷新监控
@watch_bp.route('/watch/<int:watch_id>/check', methods=['POST'])
@login_required
def check_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    space = models.Space.query.get(watch.space_id)
    if user.id != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    # 尝试在changedetection.io上立刻刷新监控
    watch_utils.update_watch_state(watch.external_id, recheck=True)
    return ok()


# 接受changedetection.io的更新通知
@watch_bp.route('/cdio/notification/change', methods=['POST'])
def process_change():
    state         = request.values.get('state')
    watch_uuid    = str(request.values.get('watch_uuid'))
    msg           = request.values.get('msg')

    watch = models.Watch.query.filter_by(external_id=watch_uuid).first()
    state_msg = ""

    # 更新失败发送失败通知
    if state == 'False':
        if msg == " ": msg = '未知错误'
        notification_msg = '监控检查失败:\n\n' + msg
        state_msg        = '检查失败: ' + msg
        if watch.notification_email:
            send_email(watch.notification_email, 
                'webmonitor-监控项获取失败通知', 
                'email/notification_fail.html', 
                watch=watch, message=notification_msg)
            
    # 更新成功则在当前快照数大于1时检查变更
    else:
        second_last_snapshot = watch_utils.get_second_latest_snapshot(watch_uuid)
        if second_last_snapshot:
            last_snapshot = watch_utils.get_latest_snapshot(watch_uuid)

            if second_last_snapshot != last_snapshot:
                # 有变更发送通知
                state_msg = '检查成功: 通知已发送'
                import difflib
                diff = difflib.HtmlDiff().make_file(second_last_snapshot.splitlines(), last_snapshot.splitlines())
                if watch.notification_email:
                    send_email(watch.notification_email, 
                        'webmonitor-监控项变更通知', 
                        'email/notification_success.html', 
                        watch=watch, diff=diff)
            else:
                state_msg = '检查成功: 无变更'
        
        else:
            state_msg = '检查成功: 初次检查'
        
    # 更新状态
    from datetime import datetime
    watch.last_check_time = datetime.now()
    watch.last_check_state = state_msg
    models.db.session.commit()
    return ok()
