import os


class BlogSettings:
    GRAVATAR_CDN_BASE = '//cdn.v2ex.com/gravatar/'
    GRAVATAR_DEFAULT_IMAGE = 'retro'
    COMMENT_STATUS = ('approved', 'pending', 'spam', 'deleted')  # TODO:评论的删除方式
    BLOG_META = {
        'name': 'Origin Blog',
        'subtitle': 'Concentration and Perseverance matter.',
        'description': os.getenv('description', 'Origin Blog Description'),
        'owner': os.getenv('owner', 'Waynerv'),
        'keywords': os.getenv('keywords', 'python,flask,web,MongoDB'),
        'index_nav1': 'About',
        'index_nav2': None,
        'bg_home': 'img/home-bg.webp',
        'bg_post': 'img/post-bg.webp',
        'bg_about': 'img/about-bg.webp',
        'display_copyright': True,
        'copyright_message': '注：转载本文，请与作者联系',
        'allow_share': True,
        'allow_donate': True,
        'donate_message': '如果觉得文章对您有价值，请作者喝杯咖啡吧',
        'donate_img_url': 'img/post-sample-image.webp',
        'dispaly_wechat': True,
        'wechat_message': '欢迎通过微信与我联系',
        'wechat_img_url': 'img/contact-bg.webp',
        'baidu_site_verification': os.getenv('baidu_site_verification', 'yOI4ewdkCY')
    }
    SOCIAL_NETWORKS = {
        'weibo': {'fa_icon': 'fab fa-weibo', 'url': None},
        'weixin': {'fa_icon': 'fab fa-weixin', 'url': None},
        'twitter': {'fa_icon': 'fab fa fa-twitter', 'url': None},
        'github': {'fa_icon': 'fab fa-github', 'url': None},
        'facebook': {'fa_icon': 'fab fa-facebook', 'url': None},
        'linkedin': {'fa_icon': 'fab fa-linkedin', 'url': None},
    }
    ROLE_PERMISSION_MAP = {
        'reader': ['COMMENT'],
        'writer': ['COMMENT', 'POST'],
        'moderator': ['COMMENT', 'POST', 'MODERATE'],
        'admin': ['COMMENT', 'POST', 'MODERATE', 'ADMINISTRATE']
    }
    SEARCH_ENGINE_SUBMIT_URLS = {
        'baidu': 'https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/form'  # TODO:Invalid URL
    }


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', '5ecret_ke9_def@ult')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_DEFAULT_SENDER = ('kaka', os.getenv('MAIL_USERNAME'))
    ORIGINBLOG_ADMIN_EMAIL = os.getenv('ORIGINBLOG_ADMIN_EMAIL')
    APP_MAIL_SUBJECT_PREFIX = 'From Origin Blog:'

    APP_POST_PER_PAGE = 10
    APP_COMMENT_PER_PAGE = 10
    APP_MANAGE_POST_PER_PAGE = 20
    APP_MANAGE_COMMENT_PER_PAGE = 20
    APP_MANAGE_USER_PER_PAGE = 20
    APP_MANAGE_WIDGET_PER_PAGE = 10
    APP_MANAGE_STATISTIC_PER_PAGE = 20
    APP_MANAGE_TRACKER_PER_PAGE = 20


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
    MONGODB_SETTINGS = {
        'db': 'originblog'
    }


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
