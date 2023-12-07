from webmonitor.watch import watch_bp
from webmonitor import models
from webmonitor.models import WatchCheckState
from flask import render_template, request, current_app
from flask_restful import Resource
from webmonitor.utils.error import ErrorCode, abort, ok
from webmonitor.utils.token import generate_token, verify_token
from webmonitor.utils.email import send_email
from webmonitor.utils.auth import login_required
import webmonitor.utils.watch as watch_utils
from webmonitor.utils.page import paginate
from datetime import datetime


# 对两个历史进行比较，返回 是否需要通知，检查信息，比较内容
def compare_watch(last_snapshot, second_last_snapshot=None, trigger_text=None):
    need_notification, check_message, html_diff = True, None, None

    # 进行比较，生成HTML文件
    import difflib
    if second_last_snapshot is None:
        html_diff = difflib.HtmlDiff().make_file([], last_snapshot.splitlines())
        check_message = "创建成功：通知已发送"
    else:
        html_diff = difflib.HtmlDiff().make_file(second_last_snapshot.splitlines(), last_snapshot.splitlines(), 
                                                 context=True, numlines=5)
        check_message = "检查成功：通知已发送"

    # 解析HTML文件获取变更内容
    add_lines, remove_lines, change_lines = [], [], []
    import bs4
    soup = bs4.BeautifulSoup(html_diff, 'html.parser')
    rows = soup.body.find('table').find_all('tr')
    for row in rows:
        _, lheader, left, _, rheader, right = row.find_all('td')
        adds = right.find_all(class_='diff_add')
        lchgs = left.find_all(class_='diff_chg')
        rchgs = right.find_all(class_='diff_chg')
        subs = left.find_all(class_='diff_sub')
        if adds:
            index = rheader.text
            text = ' '.join([add.text for add in adds])
            add_lines.append((index, text))
        if lchgs or rchgs:
            index = (lheader.text, rheader.text)
            ltext = ' '.join([chg.text for chg in lchgs])
            rtext = ' '.join([chg.text for chg in rchgs])
            change_lines.append((index, (ltext, rtext)))
        if subs:
            index = lheader.text
            text = ' '.join([sub.text for sub in subs])
            remove_lines.append((index, text))

    # 判断关键词触发
    trigger_desc = ""
    if trigger_text:
        trigger_words = [{
            'word': word.strip(),
            'count': 0,
            'indices': []
        } for word in trigger_text.split(',') if word.strip()]

        if len(trigger_words) > 0:
            # 统计触发每个关键词的行号和次数
            for word in trigger_words:
                for index, line in add_lines:
                    if word['word'] in line:
                        word['count'] += line.count(word['word'])
                        word['indices'].append(index)
                for (lindex, rindex), (old_line, new_line) in change_lines:
                    if word['word'] in new_line:
                        word['count'] += new_line.count(word['word'])
                        word['indices'].append(rindex)
        
            if not any([word['count'] > 0 for word in trigger_words]):
                # 未触发的情况，修改状态和不需要通知
                if second_last_snapshot is None:
                    check_message = "创建成功：未触发关键词"
                else:
                    check_message = "检查成功：未触发关键词"
                need_notification = False
            else:
                # 添加触发词的说明
                for word in trigger_words:
                    if word['count'] > 0:
                        word['indices'] = sorted(word['indices'])
                        trigger_desc += f"<p>关键词 \"{word['word']}\" 共出现 {word['count']} 次，出现位置: 第 {', '.join(word['indices'])} 行</p>"
    
        # 添加关键词高亮的style
        TRIGGER_WORD_STYLE = "mark {background-color: brown; color: white;}"
        soup.head.style.string = soup.head.style.text + TRIGGER_WORD_STYLE
        # 添加关键词高亮的tag
        # 防止转义
        LEFT_MARK_STR, RIGHT_MARK_STR = "$lm$", "$rm$"
        for row in rows:
            _, lheader, left, _, rheader, right = row.find_all('td')
            adds = right.find_all(class_='diff_add')
            lchgs = left.find_all(class_='diff_chg')
            rchgs = right.find_all(class_='diff_chg')
            subs = left.find_all(class_='diff_sub')
            for word in trigger_words:
                for add in adds:
                    if word['word'] in add.text:
                        add.string = add.text.replace(word['word'], f"{LEFT_MARK_STR}{word['word']}{RIGHT_MARK_STR}")
                for rchg in rchgs:
                    if word['word'] in rchg.text:
                        rchg.string = rchg.text.replace(word['word'], f"{LEFT_MARK_STR}{word['word']}{RIGHT_MARK_STR}")
        # 重新生成html
        html_diff = soup.prettify()
        html_diff = html_diff.replace(LEFT_MARK_STR, "<mark>").replace(RIGHT_MARK_STR, "</mark>")

    final_content = render_template('diff/diff_content.html', 
                                    trigger_desc=trigger_desc, 
                                    diff_content=html_diff)

    return need_notification, check_message, final_content


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
        'last_check_state': watch.last_check_message,
        'time_between_check_weeks': watch.time_between_check_weeks,
        'time_between_check_days': watch.time_between_check_days,
        'time_between_check_hours': watch.time_between_check_hours,
        'time_between_check_minutes': watch.time_between_check_minutes,
        'time_between_check_seconds': watch.time_between_check_seconds,
        'include_filters': watch.include_filters,
        'trigger_text': watch.trigger_text,
        'notification_email': watch.notification_email,
        'last_24h_check_count': watch.last_24h_check_count(),
        'last_24h_notification_count': watch.last_24h_notification_count(),
        'paused': watch.paused,
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
    watch.paused = 0
    
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
    ret = paginate(models.Watch.query.filter_by(space_id=space_id, is_deleted=0).order_by(models.Watch.create_time.desc()))
    ret.items = [{
        'id': watch.id,
        'name': watch.name,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_message,
        'last_24h_check_count': watch.last_24h_check_count(),
        'last_24h_notification_count': watch.last_24h_notification_count(),
        'paused': watch.paused,
    } for watch in ret.items]
    return ok(data=ret)


# 用户获取自己的监控列表
@watch_bp.route('/user_watches', methods=['GET'])
@login_required
def get_user_watch_list(user):
    spaces_ids = [space.id for space in user.spaces]
    ret = paginate(models.Watch.query.filter(models.Watch.space_id.in_(spaces_ids), models.Watch.is_deleted==0).order_by(models.Watch.create_time.desc()))
    ret.items = [{
        'id': watch.id,
        'name': watch.name,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_message,
        'last_24h_check_count': watch.last_24h_check_count(),
        'last_24h_notification_count': watch.last_24h_notification_count(),
        'paused': watch.paused,
    } for watch in ret.items]

    ret = {
        "total": ret.total,
        "page": ret.page,
        "size": ret.size,
        "pages": ret.pages,
        "items": ret.items,
        'today_check_count': user.today_check_count(),
        'today_notification_count': user.today_notification_count(),
        'yesterday_check_count': user.yesterday_check_count(),
        'yesterday_notification_count': user.yesterday_notification_count(),
        'this_month_check_count': user.this_month_check_count(),
        'this_month_notification_count': user.this_month_notification_count(),
    }

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

    watch_utils.update_watch_state(watch.external_id, paused=True)

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
    watch_utils.update_watch_state(watch.external_id, paused=(watch.paused==1))

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
    if not watch or watch.is_deleted == 1:
        return abort(ErrorCode.NOT_FOUND)
    
    check_state = WatchCheckState.UNKNOWN
    check_time = datetime.now()
    check_message = ""
    last_snapshot_path, second_last_snapshot_path = None, None
    diff = None

    # 无变更
    if state == 0:
        check_message = '检查成功：无变更'
        check_state = WatchCheckState.NO_CHANGE

    # 有变更
    elif state == 1:
        snapshot_list = watch_utils.get_watch_snapshot_list(watch.external_id)
        last_snapshot, second_last_snapshot = None, None
        last_snapshot_path = snapshot_list[-1]['file']
        last_snapshot = watch_utils.load_snapshot(snapshot_list[-1])
        if len(snapshot_list) > 1:
            second_last_snapshot_path = snapshot_list[-2]['file']
            second_last_snapshot = watch_utils.load_snapshot(snapshot_list[-2])

        need_notification, check_message, diff = compare_watch(last_snapshot, second_last_snapshot, watch.trigger_text)
        
        if need_notification:
            check_state = WatchCheckState.HAS_CHANGE_WITH_NOTIFICATION_SENT 

            if watch.notification_email:
                if second_last_snapshot_path:
                    send_email(watch.notification_email, 
                        'webmonitor-监控项变更通知', 
                        'email/notification_success.html', 
                        watch=watch, diff=diff)
                else:
                    send_email(watch.notification_email, 
                        'webmonitor-监控项创建通知', 
                        'email/notification_create.html', 
                        watch=watch, diff=diff, 
                        first_check_time=check_time.strftime(current_app.config['TIME_FORMAT']))
        else:
            check_state = WatchCheckState.HAS_CHANGE_NO_NOTIFICATION_SENT

    # 检查失败
    elif state == 2:
        if msg == " ": msg = '未知错误'
        notification_msg = '监控检查失败:\n\n' + msg
        check_message    = '检查失败：' + msg
        check_state      = WatchCheckState.ERROR
        if watch.notification_email:
            send_email(watch.notification_email, 
                'webmonitor-监控项获取失败通知', 
                'email/notification_fail.html', 
                watch=watch, message=notification_msg)
            
    # 未知状态
    else:
        return abort(ErrorCode.PARAMS_INVALID)
            
    # 更新最新状态
    watch.last_check_state_id = check_state.id
    watch.last_check_time = check_time
    watch.last_check_message = check_message

    # 更新历史状态
    history = models.WatchHistory()
    history.watch_id = watch.id
    history.check_state_id = check_state.id
    history.check_time = check_time
    history.check_message = check_message
    history.last_snapshot_path = last_snapshot_path
    history.second_last_snapshot_path = second_last_snapshot_path
    history.trigger_text = watch.trigger_text
    models.db.session.add(history)

    models.db.session.commit()
    
    return ok()


# 管理员获取所有的watch列表
@watch_bp.route('/watches', methods=['GET'])
@login_required
def get_all_watches(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.Watch.query.filter_by(is_deleted=0).order_by(models.Watch.create_time.desc()))
    ret.items=[{
        'id': watch.id,
        'name': watch.name,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_message,
        'notification_email': watch.notification_email,
        'last_24h_check_count': watch.last_24h_check_count(),
        'last_24h_notification_count': watch.last_24h_notification_count(),
        'paused': watch.paused,
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
        ret = paginate(models.Watch.query.filter_by(is_deleted=0).order_by(models.Watch.create_time.desc()))
    else:
        if url:
            if name:
                ret = paginate(models.Watch.query.filter(models.Watch.url.like(f'%{url}%'), models.Watch.name.like(f'%{name}%'), models.Watch.is_deleted==0).order_by(models.Watch.create_time.desc()))
            else:
                ret = paginate(models.Watch.query.filter(models.Watch.url.like(f'%{url}%'), models.Watch.is_deleted==0).order_by(models.Watch.create_time.desc()))
        else:
            ret = paginate(models.Watch.query.filter(models.Watch.name.like(f'%{name}%'), models.Watch.is_deleted==0).order_by(models.Watch.create_time.desc()))
    
    ret.items=[{
        'id': watch.id,
        'name': watch.name,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_message,
        'notification_email': watch.notification_email,
        'last_24h_check_count': watch.last_24h_check_count(),
        'last_24h_notification_count': watch.last_24h_notification_count(),
        'paused': watch.paused,
    }for watch in ret.items]
    return ok(data=ret)


# 管理员获取所有软删除的watch
@watch_bp.route('/watches/softdelete', methods=['GET'])
@login_required
def get_watches_softdeleted(user):
    if user.role != 1:
        return abort(ErrorCode.FORBIDDEN)
    ret = paginate(models.Watch.query.filter_by(is_deleted=1).order_by(models.Watch.update_time.desc()))
    ret.items=[{
        'id': watch.id,
        'name': watch.name,
        'url': watch.url,
        'create_time': watch.create_time,
        'update_time': watch.update_time,
        'last_check_time': watch.last_check_time,
        'last_check_state': watch.last_check_message,
        'notification_email': watch.notification_email,
        'last_24h_check_count': watch.last_24h_check_count(),
        'last_24h_notification_count': watch.last_24h_notification_count(),
        'space_id': watch.space_id,
        'paused': watch.paused,
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
    
    ret = models.WatchHistory.query.filter_by(watch_id=watch_id, is_deleted=0).order_by(models.WatchHistory.create_time.desc()).all()
    ret = [{
        'id': history.id,
        'create_time': history.create_time,
        'update_time': history.update_time,
        'check_time': history.check_time,
        'check_state': history.check_message,
        'check_state_id': history.check_state_id,
    } for history in ret]
    return ok(data={
        "items": ret
    })


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
        'check_state': history.check_message,
        'check_state_id': history.check_state_id,
    }

    if history.last_snapshot_path:
        last_snapshot = watch_utils.load_snapshot({'file': history.last_snapshot_path})
        second_last_snapshot = None
        if history.second_last_snapshot_path:
            second_last_snapshot = watch_utils.load_snapshot({'file': history.second_last_snapshot_path})
        _, _, content = compare_watch(last_snapshot, second_last_snapshot, history.trigger_text)
        ret['content'] = content

    return ok(data=ret)

