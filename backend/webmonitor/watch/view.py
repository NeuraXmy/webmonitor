from webmonitor.watch import watch_bp
from webmonitor import models
from flask import render_template, request, current_app
from flask_restful import Resource
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email
from webmonitor.utils.auth import login_required
import webmonitor.utils.watch as watch_utils
from webmonitor.utils.page import paginate
from datetime import datetime


# 用户获取某个监控详细信息
@watch_bp.route('/watch/<int:watch_id>', methods=['GET'])
@login_required
def get_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    space = models.Space.query.get(watch.space_id)
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    # manager or owner
    if user.role != 1 and space.owner_id != user.id: 
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
    if user.role != 1 and space.owner_id != user.id:
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
    if user.role != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    # 获取监控列表
    ret = paginate(models.Watch.query.filter_by(space_id=space_id, is_deleted=0))
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
    if user.role != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    # 删除所有历史记录
    for history in watch.watch_histories:
        models.db.session.delete(history)
    
    external_id = watch.external_id
    models.db.session.delete(watch)
    models.db.session.commit()

    # 如果数据库更新成功，在changedetection.io上删除监控
    response = watch_utils.delete_watch(external_id)
    return ok()


# 管理员软删除监控
@watch_bp.route('/watch/<int:watch_id>/softdelete', methods=['PUT'])
@login_required
def soft_delete_watch(user, watch_id):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    watch = models.Watch.query.filter_by(id=watch_id).first()
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    watch.is_deleted = 1
    models.db.session.commit()
    return ok()


# 管理员恢复监控
@watch_bp.route('/watch/<int:watch_id>/restore', methods=['PUT'])
@login_required
def restore_watch(user, watch_id):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    watch = models.Watch.query.filter_by(id=watch_id).first()
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    
    space = models.Space.query.get(watch.space_id)
    if space.is_deleted == 1:
        return abort(ErrorCode.WATCH_RESTORE_FAIL)
    
    watch.is_deleted = 0

    models.db.session.commit()
    return ok()


# 用户修改监控
@watch_bp.route('/watch/<int:watch_id>', methods=['PUT'])
@login_required
def update_watch(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    space = models.Space.query.get(watch.space_id)
    if user.role != 1 and space.owner_id != user.id:
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
    if user.role != 1 and space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    # 尝试在changedetection.io上立刻刷新监控
    watch_utils.update_watch_state(watch.external_id, recheck=True)
    return ok()


# 接受changedetection.io的刷新监控回调
@watch_bp.route('/cdio/check/callback', methods=['POST'])
def process_check_callback():
    state         = request.get_json().get('state')
    watch_uuid    = request.get_json().get('watch_uuid')
    msg           = request.get_json().get('msg')
    watch = models.Watch.query.filter_by(external_id=watch_uuid).first()
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    
    check_time = datetime.now()
    check_state = ""
    last_snapshot_path, second_last_snapshot_path = None, None

    # 无变更
    if state == 0:
        check_state = '检查成功: 无变更'

    # 有变更
    elif state == 1:
        # 获取快照路径列表，读取最新的两个快照
        snapshot_list = watch_utils.get_watch_snapshot_list(watch.external_id)
        if len(snapshot_list) > 0:
            last_snapshot_path = snapshot_list[-1]['file']
            last_snapshot = watch_utils.load_snapshot(snapshot_list[-1])
        if len(snapshot_list) > 1:
            second_last_snapshot_path = snapshot_list[-2]['file']
            second_last_snapshot = watch_utils.load_snapshot(snapshot_list[-2])
        
        if second_last_snapshot_path:
            need_notification = True
            if watch.trigger_text:
                # 关键词检测
                trigger_texts = watch.trigger_text.split(',')
                if len(trigger_texts) > 0 and not any([trigger_text in last_snapshot for trigger_text in trigger_texts]):
                    need_notification = False
                    check_state = '检查成功: 未触发关键词'

            if need_notification:
                # 有变更发送通知
                diff = watch_utils.compare_watch(last_snapshot, second_last_snapshot)
                if watch.notification_email:
                    send_email(watch.notification_email, 
                        'webmonitor-监控项变更通知', 
                        'email/notification_success.html', 
                        watch=watch, diff=diff)
                check_state = '检查成功: 通知已发送'
        else:
            # 初次检查，发送邮件
            diff = watch_utils.compare_watch(last_snapshot)
            if watch.notification_email:
                    send_email(watch.notification_email, 
                        'webmonitor-监控项初次更新通知', 
                        'email/notification_create.html', 
                        watch=watch, diff=diff, 
                        first_check_time=check_time.strftime(current_app.config['TIME_FORMAT']))
            check_state = '检查成功: 初次检查'

    # 检查失败
    elif state == 3:
        if msg == " ": msg = '未知错误'
        notification_msg = '监控检查失败:\n\n' + msg
        check_state      = '检查失败: ' + msg
        if watch.notification_email:
            send_email(watch.notification_email, 
                'webmonitor-监控项获取失败通知', 
                'email/notification_fail.html', 
                watch=watch, message=notification_msg)
            
    # 未知状态
    else:
        return abort(ErrorCode.PARAMS_INVALID)
            
    # 更新最新状态
    watch.last_check_time = check_time
    watch.last_check_state = check_state

    # 更新历史状态
    history = models.WatchHistory()
    history.watch_id = watch.id
    history.check_state = check_state
    history.check_time = check_time
    history.last_snapshot_path = last_snapshot_path
    history.second_last_snapshot_path = second_last_snapshot_path
    models.db.session.add(history)

    models.db.session.commit()
    
    return ok()


# 管理员获取所有的watch列表
@watch_bp.route('/watches', methods=['GET'])
@login_required
def get_all_watches(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.Watch.query.filter_by(is_deleted=0))
    ret.items=[{
        'id': watch.id,
        'name': watch.name,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_state,
        'notification_email': watch.notification_email
    } for watch in ret.items]
    return ok(data=ret)


# 管理员根据url或者name搜索watch
@watch_bp.route('/watches/search', methods=['GET'])
@login_required
def search_watches(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    url = request.args.get('url')
    name = request.args.get('name')
    if not any([url, name]):
        ret = paginate(models.Watch.query.filter_by(is_deleted=0))
    else:
        if url:
            if name:
                ret = paginate(models.Watch.query.filter(models.Watch.url.like(f'%{url}%'), models.Watch.name.like(f'%{name}%'), models.Watch.is_deleted==0))
            else:
                ret = paginate(models.Watch.query.filter(models.Watch.url.like(f'%{url}%'), models.Watch.is_deleted==0))
        else:
            ret = paginate(models.Watch.query.filter(models.Watch.name.like(f'%{name}%'), models.Watch.is_deleted==0))
    
    ret.items=[{
        'id': watch.id,
        'name': watch.name,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_state,
        'notification_email': watch.notification_email
    }for watch in ret.items]
    return ok(data=ret)


# 管理员获取所有软删除的watch
@watch_bp.route('/watches/softdelete', methods=['GET'])
@login_required
def get_watches_softdeleted(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.Watch.query.filter_by(is_deleted=1))
    ret.items=[{
        'id': watch.id,
        'name': watch.name,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_state,
        'notification_email': watch.notification_email,
        'space_id': watch.space_id
    }for watch in ret.items]

    i=0
    while(i<len(ret.items)):
        space = models.Space.query.get(ret.items[i]['space_id'])
        if space.is_deleted == 1:
            ret.items.remove(ret.items[i])
        else:
            i+=1
    
    for watch in ret.items:
        del watch['space_id']
    return ok(data=ret)


# 获取watch的历史记录列表
@watch_bp.route('/watch/<int:watch_id>/histories', methods=['GET'])
@login_required
def get_watch_history(user, watch_id):
    watch = models.Watch.query.get(watch_id)
    if not watch:
        return abort(ErrorCode.NOT_FOUND)
    if user.role != 1 and watch.space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    
    ret = models.WatchHistory.query.filter_by(watch_id=watch_id, is_deleted=0)
    ret = [{
        'id': history.id,
        'create_time': history.create_time,
        'update_time': history.update_time,
        'check_time': history.check_time,
        'check_state': history.check_state,
    } for history in ret]

    return ok(data=ret)


# 获取watch的历史记录详情
@watch_bp.route('/watch/<int:watch_id>/history/<int:history_id>', methods=['GET'])
@login_required
def get_watch_history_detail(user, watch_id, history_id):
    watch = models.Watch.query.get(watch_id)
    if not watch:  
        return abort(ErrorCode.NOT_FOUND)
    if user.role != 1 and watch.space.owner_id != user.id:
        return abort(ErrorCode.FORBIDDEN)
    history = models.WatchHistory.query.get(history_id)
    if not history:
        return abort(ErrorCode.NOT_FOUND)
    if history.watch_id != watch_id:
        return abort(ErrorCode.NOT_FOUND)
    
    ret = {
        'id': history.id,
        'create_time': history.create_time,
        'update_time': history.update_time,
        'check_time': history.check_time,
        'check_state': history.check_state,
    }

    # 读取快照
    if history.last_snapshot_path:
        last_snapshot, second_last_snapshot = None, None
        last_snapshot = watch_utils.load_snapshot({ 'file': history.last_snapshot_path })
        if history.second_last_snapshot_path:
            second_last_snapshot = watch_utils.load_snapshot({ 'file': history.second_last_snapshot_path })
        diff = watch_utils.compare_watch(last_snapshot, second_last_snapshot)
        ret['content'] = diff

    return ok(data=ret)

