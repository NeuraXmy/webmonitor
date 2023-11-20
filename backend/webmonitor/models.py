from webmonitor import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
    

# 基本模型
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


# 用户模型
class User(BaseModel):
    __tablename__ = "t_user"

    nickname        = db.Column(db.String(32), nullable=True)
    pwd             = db.Column(db.String(256), nullable=False)
    email           = db.Column(db.String(64), nullable=False, unique=True)
    activated       = db.Column(db.Boolean, default=False)
    activated_on    = db.Column(db.DateTime, nullable=True)

    spaces = db.relationship('Space', backref='owner', lazy=True)

    @property
    def password(self):
        return self.pwd
    
    @password.setter
    def password(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.pwd, pwd)
    

# 监控空间模型
class Space(BaseModel):
    __tablename__ = "t_space"

    name    = db.Column(db.String(32), nullable=False)
    desc    = db.Column(db.String(256), nullable=True)

    owner_id    = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)

    watches = db.relationship('Watch', backref='space', lazy=True)


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
    include_filters             = db.Column(db.String(256), nullable=True)

    last_check_time  = db.Column(db.DateTime, nullable=True)         # 上次检查的时间
    last_check_state = db.Column(db.String(256), nullable=True)      # 上次检查的状态

    notification_email = db.Column(db.String(64), nullable=True)    

    space_id    = db.Column(db.Integer, db.ForeignKey('t_space.id'), nullable=False)




