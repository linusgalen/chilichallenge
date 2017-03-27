import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = '18b*&41m!kvg3r1ydlg%(5q-8z_auzxc#v+0ev@&syclve@qim'
    SQLALCHEMY_DATABASE_URI = 'postgres://jghxcupcgfktzy:76b489e2ca955b769c5a0c0baae7fba1c5f47382f56e84aa728f72ff02a96263@ec2-176-34-186-178.eu-west-1.compute.amazonaws.com:5432/deggcqshrbsk4j'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

