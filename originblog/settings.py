import os


class BlogSettings:
    GAVATAR_CDN_BASE = 'pending'
    GAVATAR_DEFAULT_IMAGE = 'pending'
    COMMENT_STATUS = ('approved', 'pending', 'spam', 'deleted')
    BLOG_META = {
        'name': 'Origin Blog',
        'subtitle': 'Where everthing begins.',
        'description': os.getenv('description', 'Oct Blog Description'),
        'owner': os.getenv('owner', 'Waynerv'),
        'keywords': os.getenv('keywords','python,django,flask,docker,MongoDB'),
        'index_nav1': 'Donation',
        'index_nav2': 'About',
        'bg_home': 'static/img/home-bg.jpg',
        'bg_post': 'static/img/post-bg.jpg',
        'bg_about': 'static/img/about-bg.jpg',
        'display_copyright': True,
        'copyright_message': 'pending',
        'allow_share': True,
        'allow_donate': True,
        'donate_message': 'pending',
        'donate_img_url': 'pending',
        'dispaly_wechat':True,
        'wechat_message': 'pending',
        'wechat_img_url': 'pending',
        'baidu_site_verification': os.getenv('baidu_site_verification', 'yOI4ewdkCY')
    }
    SOCIAL_NETWORKS = {
        'weibo': {'fa_icon': 'fa fa-weibo', 'url': None},
        'weixin': {'fa_icon': 'fa fa-weixin', 'url': None},
        'twitter': {'fa_icon': 'fa fa fa-twitter', 'url': None},
        'github': {'fa_icon': 'fa fa-github', 'url': None},
        'facebook': {'fa_icon': 'fa fa-facebook', 'url': None},
        'linkedin': {'fa_icon': 'fa fa-linkedin', 'url': None},
    }
    ROLE_PERMISSION_MAP = {
        'reader': ['COMMENT'],
        'writer': ['COMMENT', 'POST'],
        'editor': ['COMMENT', 'POST', 'MODERATE'],
        'admin': ['COMMENT', 'POST', 'MODERATE', 'ADMINISTRATE']
    }
    SEARCH_ENGINE_SUBMIT_URLS = {
        'baidu': 'pending'
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
    ORIGINBLOG_ADMIN_EMAIL = os.getenv('ORIGINBLOG_ADMIN_EMAIL')

    ORIGINBLOG_POST_PER_PAGE = 10
    ORIGINBLOG_COMMENT_PER_PAGE = 10
    ORIGINBLOG_MANAGE_POST_PER_PAGE = 20
    ORIGINBLOG_MANAGE_COMMENT_PER_PAGE = 20
    ORIGINBLOG_MANAGE_CATEGORY_PER_PAGE = 10
    ORIGINBLOG_MANAGE_LINK_PER_PAGE = 10

    # ('theme name', 'display name')
    ORIGINLOG_THEMES = {'flatly': 'Flatly', 'united': 'United'}


class DevelopmentConfig(BaseConfig):
    # 配置mongod实例的连接
    MONGODB_SETTINGS = {
        'db': 'originblog',
        # 'host': '192.168.1.35',
        # 'port': 12345,
        # 'username': 'webapp',
        # 'password': 'pwd123'
        # 'connect': False
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
