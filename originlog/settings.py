import os


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key_default')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_LANGUAGE = 'zh-cn'

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = ('kaka', os.getenv('MAIL_USERNAME'))
    ORIGINLOG_ADMIN_EMAIL = os.getenv('ORIGINLOG_ADMIN_EMAIL')

    ORIGINLOG_POST_PER_PAGE = 10
    ORIGINLOG_MANAGE_POST_PER_PAGE = 20
    ORIGINLOG_MANAGE_COMMENT_PER_PAGE = 20
    ORIGINLOG_MANAGE_CATEGORY_PER_PAGE = 10

    # ('theme name', 'display name')
    ORIGINLOG_THEMES = {'flatly':'Flatly', 'united': 'United'}


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'TestingConfig': TestingConfig,
    'Production': ProductionConfig
}
