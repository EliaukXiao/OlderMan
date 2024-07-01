import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:152610@localhost/old_care'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
