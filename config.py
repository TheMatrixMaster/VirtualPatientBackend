import os

class Config(object):
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'msu'

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True

class ProdConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

configs = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
}
