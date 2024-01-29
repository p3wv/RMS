import os
basedir = os.path.abspath(os.path.dirname(__file__))
# dotenv_path = '/Users/dlaczegociasteczkochinskie/Desktop/INZYNIERKA/RMS/RMS/vars.env'
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'hard to guess literal string of text'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '465'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')    
    MAIL_SUPPRESS_SEND = False
    TESTING = False
    RMS_MAIL_SUBJECT_PREFIX = '[RMS]'
    RMS_MAIL_SENDER = 'Restaurant Management System Admin tornsouled@gmail.com'
    RMS_ADMIN = os.getenv('RMS_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEBUG = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
