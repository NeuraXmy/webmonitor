from webmonitor import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.dialects.mysql import LONGTEXT 
from enum import Enum
from flask import current_app


# 基本模型
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    is_deleted  = db.Column(db.Integer, nullable=False, default=0)


# 用户模型
class User(BaseModel):
    __tablename__ = "t_user"

    nickname        = db.Column(db.String(32), nullable=True)
    pwd             = db.Column(db.String(256), nullable=False)
    email           = db.Column(db.String(64), nullable=False, unique=True)
    activated       = db.Column(db.Boolean, default=False)
    activated_on    = db.Column(db.DateTime, nullable=True)
    role            = db.Column(db.Integer, nullable=False) 

    month_qta     = db.Column(db.Integer, nullable=False, default=500)     # 本月配额
    quota_exceeded  = db.Column(db.Integer, nullable=False, default=0)     # 配额是否超额
    
    spaces = db.relationship('Space', backref='owner', lazy=True)
    check_counts = db.relationship('UserCheckCount', backref='user', lazy=True)

    @property
    def password(self):
        return self.pwd
    
    @password.setter
    def password(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.pwd, pwd)

    @property
    def month_quota(self):
        return self.month_qta

    @month_quota.setter
    def month_quota(self, quota):
        self.month_qta = quota
        self.check_quota()
    
    # 增加检查次数
    def increase_check_count(self, check_state):
        current_app.logger.info(f"increase check count for user {self.id} with check_state {check_state}")
        today_check_count = UserCheckCount.query.filter(UserCheckCount.user_id == self.id, 
                                                        UserCheckCount.date == datetime.now().date()).first()
        need_add = False
        if not today_check_count:
            need_add = True
            today_check_count = UserCheckCount(user_id=self.id, date=datetime.now().date(),
                                               silent_count=0, notification_count=0, error_count=0) 
        if check_state == WatchCheckState.NO_CHANGE:
            today_check_count.silent_count += 1
        elif check_state == WatchCheckState.HAS_CHANGE_WITH_NOTIFICATION_SENT:
            today_check_count.notification_count += 1
        elif check_state == WatchCheckState.HAS_CHANGE_NO_NOTIFICATION_SENT:
            today_check_count.silent_count += 1
        elif check_state == WatchCheckState.ERROR:
            today_check_count.error_count += 1
        if need_add:
            db.session.add(today_check_count)
        

    def today_check_count(self):
        return sum([c.silent_count + c.notification_count + c.error_count for c in self.check_counts 
                    if c.date == datetime.now().date()])

    def today_notification_count(self):
        return sum([c.notification_count for c in self.check_counts
                    if c.date == datetime.now().date()])
    
    def yesterday_check_count(self):
        return sum([c.silent_count + c.notification_count + c.error_count for c in self.check_counts
                    if c.date == datetime.now().date() - timedelta(days=1)])
    
    def yesterday_notification_count(self):
        return sum([c.notification_count for c in self.check_counts
                    if c.date == datetime.now().date() - timedelta(days=1)])
    
    def this_month_check_count(self):
        return sum([c.silent_count + c.notification_count + c.error_count for c in self.check_counts
                    if c.date.month == datetime.now().month])
        
    def this_month_notification_count(self):
        return sum([c.notification_count for c in self.check_counts
                    if c.date.month == datetime.now().month])
    
    # 进行配额检查, 如果超过配额, 暂停所有监控，否则恢复所有监控
    def check_quota(self):
        check_count = self.this_month_check_count()
        current_app.logger.info(f"check quota for user {self.id}, month_qta={self.month_qta} check_count={check_count}, quota_exceeded={self.quota_exceeded}")
        if self.quota_exceeded == 0:
            if check_count >= self.month_qta:
                self.quota_exceeded = 1
                for space in self.spaces:
                    for watch in space.watches:
                        watch.quota_exceeded = 1
                        watch.sync_cdio_pause()
        else:
            if check_count < self.month_qta:
                self.quota_exceeded = 0
                for space in self.spaces:
                    for watch in space.watches:
                        watch.quota_exceeded = 0
                        watch.sync_cdio_pause()


# 用户每日检查次数模型
class UserCheckCount(BaseModel):
    __tablename__ = "t_user_check_count"

    user_id           = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)
    date              = db.Column(db.Date, nullable=False)

    silent_count       = db.Column(db.Integer, nullable=False, default=0) # 未通知次数
    notification_count = db.Column(db.Integer, nullable=False, default=0) # 已通知次数
    error_count        = db.Column(db.Integer, nullable=False, default=0) # 错误次数


# 监控空间模型
class Space(BaseModel):
    __tablename__ = "t_space"

    name    = db.Column(db.String(32), nullable=False)
    desc    = db.Column(db.String(256), nullable=True)

    owner_id    = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)

    watches = db.relationship('Watch', backref='space', lazy=True)
    check_counts = db.relationship('SpaceCheckCount', backref='space', lazy=True)

    # 增加检查次数
    def increase_check_count(self, check_state):
        current_app.logger.info(f"increase check count for space {self.id} with check_state {check_state}")
        today_check_count = SpaceCheckCount.query.filter(SpaceCheckCount.space_id == self.id, 
                                                         SpaceCheckCount.date == datetime.now().date()).first()
        need_add = False
        if not today_check_count:
            need_add = True
            today_check_count = SpaceCheckCount(space_id=self.id, date=datetime.now().date(),
                                                silent_count=0, notification_count=0, error_count=0) 
        if check_state == WatchCheckState.NO_CHANGE:
            today_check_count.silent_count += 1
        elif check_state == WatchCheckState.HAS_CHANGE_WITH_NOTIFICATION_SENT:
            today_check_count.notification_count += 1
        elif check_state == WatchCheckState.HAS_CHANGE_NO_NOTIFICATION_SENT:
            today_check_count.silent_count += 1
        elif check_state == WatchCheckState.ERROR:
            today_check_count.error_count += 1
        if need_add:
            db.session.add(today_check_count)

    def today_check_count(self):
        return sum([c.silent_count + c.notification_count + c.error_count for c in self.check_counts 
                    if c.date == datetime.now().date()])
    
    def today_notification_count(self):
        return sum([c.notification_count for c in self.check_counts 
                    if c.date == datetime.now().date()])

    def yesterday_check_count(self):
        return sum([c.silent_count + c.notification_count + c.error_count for c in self.check_counts 
                    if c.date == datetime.now().date() - timedelta(days=1)])
    
    def yesterday_notification_count(self):  
        return sum([c.notification_count for c in self.check_counts 
                    if c.date == datetime.now().date() - timedelta(days=1)])
    
    def this_month_check_count(self):
        return sum([c.silent_count + c.notification_count + c.error_count for c in self.check_counts 
                    if c.date.month == datetime.now().month])
    
    def this_month_notification_count(self):
        return sum([c.notification_count for c in self.check_counts 
                    if c.date.month == datetime.now().month])


# 空间每日检查次数模型
class SpaceCheckCount(BaseModel):
    __tablename__ = "t_space_check_count"

    space_id           = db.Column(db.Integer, db.ForeignKey('t_space.id'), nullable=False)
    date               = db.Column(db.Date, nullable=False)

    silent_count       = db.Column(db.Integer, nullable=False, default=0) # 未通知次数
    notification_count = db.Column(db.Integer, nullable=False, default=0) # 已通知次数
    error_count        = db.Column(db.Integer, nullable=False, default=0) # 错误次数


# 检查状态枚举值
class WatchCheckState(Enum):
    UNKNOWN                             = (0)
    NO_CHANGE                           = (1)
    HAS_CHANGE_WITH_NOTIFICATION_SENT   = (2)
    HAS_CHANGE_NO_NOTIFICATION_SENT     = (3)
    ERROR                               = (4)
    def __init__(self, id) -> None:
        self.id = id


# 监控项模型
class Watch(BaseModel):
    __tablename__ = "t_watch"

    name    = db.Column(db.String(32), nullable=False)
    desc    = db.Column(db.String(256), nullable=True)

    url     = db.Column(db.String(256), nullable=False)

    external_id = db.Column(db.String(64), nullable=True)   # changedetection.io的id

    time_between_check_weeks    = db.Column(db.Integer, nullable=False, default=0)
    time_between_check_days     = db.Column(db.Integer, nullable=False, default=0)
    time_between_check_hours    = db.Column(db.Integer, nullable=False, default=0)
    time_between_check_minutes  = db.Column(db.Integer, nullable=False, default=0)
    time_between_check_seconds  = db.Column(db.Integer, nullable=False, default=0)
    include_filters             = db.Column(db.String(1024), nullable=True)
    trigger_text                = db.Column(db.String(1024), nullable=True)
    paused                      = db.Column(db.Integer, nullable=False, default=0)  # 是否被用户手动暂停
    quota_exceeded              = db.Column(db.Integer, nullable=False, default=0)  # 配额是否超额
    cdio_paused                 = db.Column(db.Integer, nullable=False, default=0)  # 在changedetection.io上是否暂停

    last_check_state_id = db.Column(db.Integer, nullable=True)          # 上次检查的状态id
    last_check_time     = db.Column(db.DateTime, nullable=True)         # 上次检查的时间
    last_check_message  = db.Column(db.String(256), nullable=True)      # 上次检查的状态信息

    notification_email = db.Column(db.String(64), nullable=True)    

    space_id    = db.Column(db.Integer, db.ForeignKey('t_space.id'), nullable=False)

    watch_histories = db.relationship('WatchHistory', backref='watch', lazy=True)

    # 同步cdio上的pause状态
    def sync_cdio_pause(self):
        current_app.logger.info(f"sync cdio pause state for watch {self.id}, external_id={self.external_id}, cdio_paused={self.cdio_paused} paused={self.paused} quota_exceeded={self.quota_exceeded} is_deleted={self.is_deleted}")
        import webmonitor.utils.watch as watch_utils
        if self.cdio_paused == 0:
            if self.paused == 1 or self.quota_exceeded == 1 or self.is_deleted == 1:
                self.cdio_paused = 1
                watch_utils.update_watch_state(self.external_id, paused=True)
        else:
            if self.paused == 0 and self.quota_exceeded == 0 and self.is_deleted == 0:
                self.cdio_paused = 0
                watch_utils.update_watch_state(self.external_id, paused=False)

    def today_check_count(self):
        return WatchHistory.query.filter(WatchHistory.watch_id == self.id, 
                                         WatchHistory.check_time > datetime.now().replace(hour=0, minute=0, second=0)).count()

    def today_notification_count(self):
        return WatchHistory.query.filter(WatchHistory.watch_id == self.id, 
                                         WatchHistory.check_time > datetime.now().replace(hour=0, minute=0, second=0),
                                         WatchHistory.check_state_id == WatchCheckState.HAS_CHANGE_WITH_NOTIFICATION_SENT.id).count()

    def yesterday_check_count(self):
        return WatchHistory.query.filter(WatchHistory.watch_id == self.id, 
                                         WatchHistory.check_time > datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1),
                                         WatchHistory.check_time < datetime.now().replace(hour=0, minute=0, second=0)).count()
    
    def yesterday_notification_count(self):
        return WatchHistory.query.filter(WatchHistory.watch_id == self.id, 
                                         WatchHistory.check_time > datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1),
                                         WatchHistory.check_time < datetime.now().replace(hour=0, minute=0, second=0),
                                         WatchHistory.check_state_id == WatchCheckState.HAS_CHANGE_WITH_NOTIFICATION_SENT.id).count()

    def this_month_check_count(self):
        return WatchHistory.query.filter(WatchHistory.watch_id == self.id, 
                                         WatchHistory.check_time > datetime.now().replace(day=1, hour=0, minute=0, second=0)).count()
    
    def this_month_notification_count(self):
        return WatchHistory.query.filter(WatchHistory.watch_id == self.id, 
                                         WatchHistory.check_time > datetime.now().replace(day=1, hour=0, minute=0, second=0),
                                         WatchHistory.check_state_id == WatchCheckState.HAS_CHANGE_WITH_NOTIFICATION_SENT.id).count()

    def last_24h_check_count(self):
        return WatchHistory.query.filter(WatchHistory.watch_id == self.id, 
                                         WatchHistory.check_time > datetime.now() - timedelta(days=1)).count()
    
    def last_24h_notification_count(self):
        return WatchHistory.query.filter(WatchHistory.watch_id == self.id, 
                                         WatchHistory.check_time > datetime.now() - timedelta(days=1),
                                         WatchHistory.check_state_id == WatchCheckState.HAS_CHANGE_WITH_NOTIFICATION_SENT.id).count()
        

# 监控项检查记录模型
class WatchHistory(BaseModel):
    __tablename__ = "t_watch_history"

    check_state_id = db.Column(db.Integer, nullable=True)              # 检查的状态id
    check_time     = db.Column(db.DateTime, nullable=True)             # 检查的时间
    check_message  = db.Column(db.String(256), nullable=True)          # 检查的状态信息

    trigger_text = db.Column(db.String(1024), nullable=True)    # 检查时监控的触发词

    last_snapshot_path        = db.Column(db.String(256), nullable=True)    # 检查的快照路径
    second_last_snapshot_path = db.Column(db.String(256), nullable=True)    # 上次检查的快照路径

    watch_id    = db.Column(db.Integer, db.ForeignKey('t_watch.id'), nullable=False)