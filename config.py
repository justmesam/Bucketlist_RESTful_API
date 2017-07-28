import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG=False
    SECRET_KEY='\x86\x99\x13Q\xd3\xb56d\xcb\xbb4rf:\xf4W\xdf?\xe3\xb2\x06U\x1b\xe2'
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']

class DevelopmentConfig(Config):
    DEBUG=True
