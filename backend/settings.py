# what_to_watch/settings.py
import os

basedir = os.path.abspath(os.path.dirname(__file__)) # Тут добавили

class Config(object):
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DATABASE")}'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    UPLOADED_IMAGES_DEST = os.path.join(basedir, 'opinions_app/media') # Тут добавили
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')