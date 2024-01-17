from webmonitor import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.dialects.mysql import LONGTEXT 
from enum import Enum
from flask import current_app


# 获取某个时间的下个月当天
def get_next_month_day(date):
    year = date.year
    month = date.month
    day = date.day
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    return datetime(year, month, day)

# 获取某个时间的下一年当天
def get_next_year_day(date):
    year = date.year
    month = date.month
    day = date.day
    return datetime(year+1, month, day)



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

    quota_exceeded  = db.Column(db.Integer, nullable=False, default=0)      # 配额是否超额
    stripe_customer_id = db.Column(db.String(256), nullable=True)           # stripe的customer id

    inviter_code = db.Column(db.String(32), nullable=True)          # 自己的邀请码
    invitee_code = db.Column(db.String(32), nullable=True)          # 使用的邀请码 NULL表示没有使用邀请码
    
    spaces = db.relationship('Space', backref='owner', lazy=True)
    check_counts = db.relationship('UserCheckCount', backref='user', lazy=True)


    @property
    def password(self):
        return self.pwd
    
    @password.setter
    def password(self, pwd):
        self.pwd = generate_password_hash(pwd)

    # 检查密码是否正确
    def check_password(self, pwd):
        return check_password_hash(self.pwd, pwd)


    # 获取当前正在被使用的套餐（有效套餐中最早过期的一个）
    def get_current_package(self):
        available_packages = [p for p in self.packages if not p.is_expired()]
        available_packages.sort(key=lambda p: p.current_period_end_time)
        if len(available_packages) > 0:
            return available_packages[0]
        return None

    # 增加检查次数，并且消耗套餐的配额（之后需要调用check_quota）
    def increase_check_count(self, check_state):
        current_app.logger.info(f"increase check count for user {self.id} with check_state {check_state}")

        # 添加checkcount记录
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

        # 消耗套餐的配额
        package = self.get_current_package()
        if package is not None:
            package.check_count_left -= 1
            current_app.logger.info(f"use package {package.id} for user {self.id}, check_count_left={package.check_count_left}")

    # 进行配额检查, 如果超过配额, 暂停所有监控，否则恢复所有监控
    # 在所有配额需要更新的地方调用：添加/删除套餐，套餐更新，套餐配额消耗
    def check_quota(self):
        current_app.logger.info(f"check quota for user {self.id}, quota_exceeded={self.quota_exceeded}")

        has_quota = (self.get_current_package() is not None)
        
        if self.quota_exceeded == 0 and not has_quota:
            self.quota_exceeded = 1
            for space in self.spaces:
                for watch in space.watches:
                    watch.quota_exceeded = 1
                    watch.sync_cdio_pause()
        if self.quota_exceeded == 1 and has_quota:
            self.quota_exceeded = 0
            for space in self.spaces:
                for watch in space.watches:
                    watch.quota_exceeded = 0
                    watch.sync_cdio_pause()


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



# 用户邀请记录模型
class UserInvitation(BaseModel):
    __tablename__ = "t_user_invitation"

    inviter_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False) # 邀请者id
    invitee_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False) # 被邀请者id
    invitee_email = db.Column(db.String(64), nullable=False)                       # 被邀请者邮箱

    inviter = db.relationship('User', foreign_keys=[inviter_id], backref='invitations', lazy=True)
    invitee = db.relationship('User', foreign_keys=[invitee_id], backref='invited_by', lazy=True)



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



# 套餐周期类型枚举值
class PackagePeriodType(Enum):
    PERMANENT   = (0, '单次永久')   
    DAY         = (1, '日付')   
    MONTH       = (2, '月付')  
    YEAR        = (3, '年付') 
    TEST        = (4, '测试')

    def __init__(self, id, desc) -> None:
        self.id = id
        self.desc = desc
    
    @staticmethod
    def get_desc_by_id(id):
        for period_type in PackagePeriodType:
            if period_type.id == id:
                return period_type.desc
        return None

    # 获取下一个周期的开始时间
    @staticmethod
    def get_next_time(period_type_id, current_time):
        if period_type_id == PackagePeriodType.PERMANENT.id:
            return current_time + timedelta(days=365*1000)
        elif period_type_id == PackagePeriodType.DAY.id:
            return current_time + timedelta(days=1)
        elif period_type_id == PackagePeriodType.MONTH.id:
            return get_next_month_day(current_time)
        elif period_type_id == PackagePeriodType.YEAR.id:
            return get_next_year_day(current_time)
        elif period_type_id == PackagePeriodType.TEST.id:
            return current_time + timedelta(minutes=1)
        return None
        


# 套餐模板模型
class PackageTemplate(BaseModel):
    __tablename__ = "t_package_template"

    name    = db.Column(db.String(32), nullable=False)
    period_type         = db.Column(db.Integer, nullable=False, default=0)  # 套餐周期类型
    period_check_count  = db.Column(db.Integer, nullable=False, default=0)  # 一次周期内给予的检查次数
    price = db.Column(db.Integer, nullable=False, default=0)                # 套餐价格（单位为分人民币）

    hide    = db.Column(db.Integer, nullable=False, default=0)              # 是否对用户隐藏
    initial = db.Column(db.Integer, nullable=False, default=0)              # 是否是初始套餐

    inviter_package = db.Column(db.Integer, nullable=False, default=0)      # 是否赠送给邀请者
    invitee_package = db.Column(db.Integer, nullable=False, default=0)      # 是否赠送给被邀请者



# 用户套餐模型
class Package(BaseModel):
    __tablename__ = "t_package"

    user_id     = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)

    name    = db.Column(db.String(32), nullable=False)                      
    period_type         = db.Column(db.Integer, nullable=False, default=0)  # 套餐周期类型
    period_check_count  = db.Column(db.Integer, nullable=False, default=0)  # 一次周期内给予的检查次数
    price = db.Column(db.Integer, nullable=False, default=0)                # 套餐价格（单位为分人民币）

    start_time  = db.Column(db.DateTime, nullable=True)                # 开始时间
    current_period_start_time = db.Column(db.DateTime, nullable=True)  # 当前周期开始时间
    current_period_end_time   = db.Column(db.DateTime, nullable=True)  # 当前周期结束时间
    check_count_left = db.Column(db.Integer, nullable=True)            # 当前周期剩余检查次数

    cancel_at_next           = db.Column(db.Integer, nullable=False, default=0)  # 是否在下个周期取消续订
    need_payment             = db.Column(db.Integer, nullable=False, default=0)  # 是否需要付款
    is_last_payment_failed   = db.Column(db.Integer, nullable=True, default=0)   # 上次付款是否失败

    current_period_notified = db.Column(db.Integer, nullable=False, default=0)   # 当前周期是否已经通知过

    stripe_payment_method_id = db.Column(db.String(256), nullable=True)          # stripe的付款方式id

    user = db.relationship('User', backref='packages', lazy=True)

    # 套餐是否不可用（付款失败、配额超额、被删除）
    def is_expired(self):
        if self.is_deleted:
            return True
        if self.need_payment and self.is_last_payment_failed == 1:
            return True
        if self.check_count_left is not None and self.check_count_left <= 0:
            return True
        return False


# 套餐付款状态枚举值
class PackagePaymentStatus(Enum):
    CREATED     = (0)   # 已创建
    PENDING     = (1)   # 待付款
    SUCCEEDED   = (2)   # 付款成功
    FAILED      = (3)   # 付款失败
    REFUND      = (4)   # 已退款

    def __init__(self, id) -> None:
        self.id = id



# 套餐付款模型
class PackagePayment(BaseModel):
    __tablename__ = "t_package_payment"

    stripe_payment_intent_id = db.Column(db.String(256), nullable=True)      # stripe的付款意图id

    name     = db.Column(db.String(32), nullable=False)                        # 付款描述
    status   = db.Column(db.Integer, nullable=False, default=0)                # 付款状态
    msg      = db.Column(db.String(512), nullable=True)                        # 付款状态信息
    pay_time = db.Column(db.DateTime, nullable=True)                           # 付款时间
    amount   = db.Column(db.Integer, nullable=False, default=0)                # 付款金额（单位为分人民币）

    package_id = db.Column(db.Integer, db.ForeignKey('t_package.id'), nullable=False)
    package = db.relationship('Package', backref='payments', lazy=True)
