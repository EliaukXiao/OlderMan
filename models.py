from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
class OldPersonInfo(db.Model):
    __tablename__ = 'oldperson_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(5), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    id_card = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    checkin_date = db.Column(db.DateTime, nullable=False)
    checkout_date = db.Column(db.DateTime, nullable=True)
    imgset_dir = db.Column(db.String(200), nullable=True, default=None)  # 使用None作为默认值
    room_number = db.Column(db.String(50), nullable=False)
    firstguardian_name = db.Column(db.String(50), nullable=False)
    firstguardian_relationship = db.Column(db.String(50), nullable=False)
    firstguardian_phone = db.Column(db.String(50), nullable=False)
    firstguardian_wechat = db.Column(db.String(50), nullable=False)
    secondguardian_name = db.Column(db.String(50), nullable=False)
    secondguardian_relationship = db.Column(db.String(50), nullable=False)
    secondguardian_phone = db.Column(db.String(50), nullable=False)
    secondguardian_wechat = db.Column(db.String(50), nullable=False)
    health_state = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        data = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        if not data['imgset_dir']:
            data['imgset_dir'] = '/static/orderMan.jpg'  # 默认图像路径
        return data
class EmployeeInfo(db.Model):
    __tablename__ = 'employee_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    gender = db.Column(db.String(5))
    phone = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)
    hire_date = db.Column(db.DateTime)
    resign_date = db.Column(db.DateTime)
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    description = db.Column(db.String(200))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class VolunteerInfo(db.Model):
    __tablename__ = 'volunteer_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    gender = db.Column(db.String(5))
    phone = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)
    checkin_date = db.Column(db.DateTime)
    checkout_date = db.Column(db.DateTime)
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class EventInfo(db.Model):
    __tablename__ = 'event_info'
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.Integer)
    event_date = db.Column(db.DateTime)
    event_location = db.Column(db.String(200))
    event_desc = db.Column(db.String(200))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # 增加长度以存储加密密码
    real_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)  # 使用 '0' 表示女性，'1' 表示男性
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}