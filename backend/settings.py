# what_to_watch/settings.py
import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DATABASE")}'
    SECRET_KEY = os.getenv('SECRET_KEY')