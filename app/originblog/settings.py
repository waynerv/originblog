import os
from originblog.utils import get_boolean_from_env, get_int_from_env


class BlogSettings:
    # 博客内容配置
    GRAVATAR_CDN_BASE = '//cdn.v2ex.com/gravatar/'
    GRAVATAR_DEFAULT_IMAGE = 'retro'
    COMMENT_STATUS = ('approved', 'pending', 'spam', 'deleted')  # TODO:评论的删除方式
    BLOG_META = {
        'name': os.getenv('name', 'Origin Blog'),
        'subtitle': os.getenv('subtitle', 'Concentration and Perseverance matter.'),
        'description': os.getenv('description', 'Origin Blog Description'),
        'owner': os.getenv('owner', 'Waynerv'),
        'keywords': os.getenv('keywords', 'python,flask,web,MongoDB'),
        'index_nav1': 'About',
        'index_nav2': None,
        'bg_home': os.getenv('bg_home', '../../static/img/home-bg.webp'),
        'bg_post': os.getenv('bg_post', '../../static/img/post-bg.webp'),
        'bg_about': os.getenv('bg_about', '../../static/img/about-bg.webp'),
        'display_copyright': True,
        'copyright_message': '注：转载本文，请与作者联系',
        'allow_share': True,
        'allow_donate': True,
        'donate_message': '如果觉得文章对您有价值，请作者喝杯咖啡吧',
        'donate_img_url': os.getenv('donate_img_url', '../../static/img/post-sample-image.webp'),
        'dispaly_wechat': True,
        'wechat_message': '欢迎通过微信与我联系',
        'wechat_img_url': os.getenv('wechat_img_url', '../../static/img/contact-bg.webp'),
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
        'baidu': os.getenv('baidu_submit_url', 'https://developer.mozilla.org')
    }


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig(object):
    # 程序密钥
    SECRET_KEY = os.getenv('SECRET_KEY', '5ecr07_ke9_def@u1t')

    # 发送邮件相关配置,此处使用了SendGrid
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = get_boolean_from_env('MAIL_USE_TLS', 'True')
    MAIL_PORT = get_int_from_env('MAIL_PORT', 587)
    MAIL_DEFAULT_SENDER = ('Admin', os.getenv('MAIL_USERNAME'))
    APP_MAIL_SUBJECT_PREFIX = 'From Origin Blog:'

    # 管理员邮件地址，以此邮箱可注册为管理员
    ORIGINBLOG_ADMIN_EMAIL = os.getenv('ORIGINBLOG_ADMIN_EMAIL', 'originblog@admin.com')

    # 内容分页配置
    APP_POST_PER_PAGE = 10
    APP_COMMENT_PER_PAGE = 10
    APP_MANAGE_POST_PER_PAGE = 20
    APP_MANAGE_COMMENT_PER_PAGE = 20
    APP_MANAGE_USER_PER_PAGE = 20
    APP_MANAGE_WIDGET_PER_PAGE = 10
    APP_MANAGE_STATISTIC_PER_PAGE = 20
    APP_MANAGE_TRACKER_PER_PAGE = 20


class DevelopmentConfig(BaseConfig):
    # 连接mongod实例的配置
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
    # 部署环境需要使用用户密码连接
    MONGODB_SETTINGS = {
        'db': os.getenv('DB_NAME', 'originblog'),
        'host': os.getenv('MONGO_HOST', 'localhost'),
        'port': get_int_from_env('MONGO_PORT', 27017),
        'username': os.getenv('MONGODB_ADMINUSERNAME', 'originblog'),
        'password': os.getenv('MONGODB_ADMINPASSWORD', 'PASSWORD')
    }


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
