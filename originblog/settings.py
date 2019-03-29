import os


class BlogSettings:
    GAVATAR_CDN_BASE = 'pending'
    GAVATAR_DEFAULT_IMAGE = 'pending'
    COMMENT_STATUS = ('approved', 'pending', 'spam', 'deleted')
    BLOG_META = {
        'name': 'Origin Blog',
        'subtitle': 'Where everthing begins.',
        'bg_home': 'static/img/home_bg.jpg',
        'bg_post': 'static/img/post_bg.jpg',
        'display_copyright': True,
        'copyright_message': 'pending',
        'allow_share': True,
        'allow_donate': True,
        'donate_message': 'pending',
        'donate_img_url': 'pending',
        'dispaly_wechat':True,
        'wechat_message': 'pending',
        'wechat_img_url': 'pending,'
    }


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key_default')

    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_LANGUAGE = 'zh-cn'
    CKEDITOR_HEIGHT = 300

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
    ORIGINLOG_MANAGE_LINK_PER_PAGE = 10

    # ('theme name', 'display name')
    ORIGINLOG_THEMES = {'flatly': 'Flatly', 'united': 'United'}


class DevelopmentConfig(BaseConfig):
    MONGODB_SETTINGS = {
        'db': 'oringinblog',
    }


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
