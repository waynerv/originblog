import os


class BlogSettings:
    GRAVATAR_CDN_BASE = '//cdn.v2ex.com/gravatar/'
    GRAVATAR_DEFAULT_IMAGE = 'http://7tsygu.com1.z0.glb.clouddn.com/user-avatar.jpg'
    COMMENT_STATUS = ('approved', 'pending', 'spam', 'deleted')
    BLOG_META = {
        'name': 'Origin Blog',
        'subtitle': 'Where everthing begins.',
        'description': os.getenv('description', 'Oct Blog Description'),
        'owner': os.getenv('owner', 'Waynerv'),
        'keywords': os.getenv('keywords','python,django,flask,docker,MongoDB'),
        'index_nav1': 'Donation',
        'index_nav2': 'About',
        'bg_home': 'img/home-bg.jpg',
        'bg_post': 'img/post-bg.jpg',
        'bg_about': 'img/about-bg.jpg',
        'display_copyright': True,
        'copyright_message': '注：转载本文，请与作者联系',
        'allow_share': True,
        'allow_donate': True,
        'donate_message': '如果觉得文章对您有价值，请作者喝杯咖啡吧',
        'donate_img_url': 'img/post-sample-image.jpg',
        'dispaly_wechat':True,
        'wechat_message': '欢迎通过微信与我联系',
        'wechat_img_url': 'img/post-sample-image.jpg',
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
        'moderator': ['COMMENT', 'POST', 'MODERATE'],
        'admin': ['COMMENT', 'POST', 'MODERATE', 'ADMINISTRATE']
    }
    SEARCH_ENGINE_SUBMIT_URLS = {
        'baidu': 'https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/form'
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
    APP_MAIL_SUBJECT_PREFIX = 'From Origin Blog:'

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
