import hashlib
import re
from datetime import datetime
from urllib.parse import urlencode

import bleach
import markdown2
from flask import current_app
from flask_login import UserMixin
from itsdangerous import BadTimeSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from unidecode import unidecode
from werkzeug.security import generate_password_hash, check_password_hash

from originblog.extensions import db
from originblog.settings import BlogSettings
from originblog.settings import Operations

# 获取博客配置
COMMENT_STATUS = BlogSettings.COMMENT_STATUS
GRAVATAR_CDN_BASE = BlogSettings.GRAVATAR_CDN_BASE
GRAVATAR_DEFAULT_IMAGE = BlogSettings.GRAVATAR_DEFAULT_IMAGE
SOCIAL_NETWORKS = BlogSettings.SOCIAL_NETWORKS
ROLE_PERMISSION_MAP = BlogSettings.ROLE_PERMISSION_MAP

# 编译分割标题获取别名的正则表达式
_punct_re = re.compile(r'[\t !"#$%&\-/<=>?@\[\\\]^_`{|},.]+')


def get_clean_html_content(html_content):
    """对转换成HTML的markdown文本进行消毒"""
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'br', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'hr', 'img',
                    'table', 'thead', 'tbody', 'tr', 'th', 'td',
                    'sup', 'sub']
    allowed_attrs = {
        '*': ['class'],
        'a': ['href', 'rel', 'name'],
        'img': ['alt', 'src', 'title']
    }
    html_content = bleach.linkify(bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attrs, strip=True))
    return html_content


def slugify(text, delim=u'-'):
    """Generates a ASCII-only slug"""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).lower().split())
    return unidecode(delim.join(result))[:230]


class Role(db.Document):
    """定义角色与权限模型"""
    role_name = db.StringField(default='reader')
    permissions = db.ListField(db.StringField(unique=True))

    @classmethod
    def init(cls):
        """初始化角色与对应的权限，支持角色的增加和更新"""
        for role_name in ROLE_PERMISSION_MAP:
            role = cls.objects.filter(role_name=role_name).first()
            if role is None:
                role = cls(role_name=role_name)
            role.permissions = []  # 每次初始化都清空角色权限
            for permission in ROLE_PERMISSION_MAP[role_name]:
                role.permissions.append(permission)
            role.save()


class User(db.Document, UserMixin):
    """定义用户数据模型"""
    username = db.StringField(max_length=20, required=True, unique=True)
    password_hash = db.StringField(max_length=128, required=True)
    name = db.StringField(max_length=30, default=username)
    email = db.EmailField(max_length=255, required=True, unique=True)
    create_time = db.DateTimeField(default=datetime.utcnow, required=True)
    last_login = db.DateTimeField(default=datetime.utcnow, required=True)
    email_confirmed = db.BooleanField(default=False)
    role = db.ReferenceField('Role')  # TODO:角色被删除后的级联行为，目前角色不可删除
    bio = db.StringField(max_length=200)
    homepage = db.StringField(max_length=255)
    social_networks = db.DictField(default=SOCIAL_NETWORKS)
    active = db.BooleanField(default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Flask Login所需要实现的取得有效ID的方法"""
        try:
            return self.username
        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')

    def generate_token(self, operation, expire_in=None, **kwargs):
        """生成私密操作所需要的验证token。

        使用itsdangerous提供的jws序列化器将用户信息、操作类型等序列化成token
        :param self: 用户对象
        :param operation: 操作类型 Operations 类属性
        :param expire_in: 过期时间（秒），默认值None时为一个小时
        :param kwargs: 其他需要序列化的关键字参数（如新的邮箱地址）
        :return: 序列化生成的token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expire_in)  # 接收密钥和过期时间（秒）参数实例化一个JWS序列化器对象
        data = {
            'username': self.username,
            'operation': operation
        }
        data.update(**kwargs)
        return s.dumps(data)

    def validate_token(self, token, operation, new_password=None):
        """验证token，并根据token携带的数据执行相应操作。

        :param self: 用户对象
        :param token: token字符串
        :param operation: 要验证的操作类型（确认邮箱、重置密码或修改邮箱）
        :param new_password: 若操作类型为重置密码可将新密码作为参数传入
        :return: 布尔值
        """
        s = Serializer(current_app.config['SECRET_KEY'])

        # 尝试获取token中被序列化的信息，token不一定合法，应使用try...except语句
        try:
            data = s.loads(token)
        except (BadTimeSignature, SignatureExpired):
            return False

        # 验证token携带的用户名和操作类型是否相符
        if operation != data.get('operation') or self.username != data.get('username'):
            return False

        # 根据不同的操作类型执行对应操作
        if operation == Operations.CONFIRM:
            self.email_confirmed = True
        elif operation == Operations.RESET_PASSWORD:
            self.set_password(new_password)
        elif operation == Operations.CHANGE_EMAIL:
            self.email = data.get('new_email')
        else:
            return False

        self.save()
        return True

    @property
    def is_admin(self):
        """检查用户是否拥有管理员权限"""
        return self.role and self.role.role_name == 'admin'

    @property
    def is_active(self):
        """Flask-Login检查用户是否活跃"""
        return self.active

    @property
    def posts_count(self):
        """发表的文章总数"""
        return Post.objects.filter(author=self).count()

    def can(self, permission):
        """检查用户是否拥有指定权限"""
        return self.role and permission in self.role.permissions

    def set_role(self):
        """除网站管理员外，为每个用户指定初始角色为reader"""
        if self.email != current_app.config['ORIGINBLOG_ADMIN_EMAIL']:
            self.role = Role.objects.filter(role_name='reader').first()
        else:
            self.role = Role.objects.filter(role_name='admin').first()

    def clean(self):
        """在创建对象并写入到数据库之前为其设置角色"""
        if not self.role:
            self.set_role()

    meta = {
        'indexes': ['username'],
    }


class Post(db.Document):
    """定义文章数据模型"""
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    abstract = db.StringField(max_length=255)
    author = db.ReferenceField('User', reverse_delete_rule=db.CASCADE)  # 用户被删除时，关联的文章也会被删除
    raw_content = db.StringField(required=True)
    html_content = db.StringField(required=True)
    pub_time = db.DateTimeField()
    update_time = db.DateTimeField()
    category = db.StringField(max_length=64, default='default')
    tags = db.ListField(db.StringField(max_length=30))
    weight = db.IntField(default=10)
    can_comment = db.BooleanField(default=True)
    from_admin = db.BooleanField(default=False)
    type = db.StringField(max_length=64, default='post')  # 将使用'page'类型保存捐赠、博客介绍等专用页面

    def set_slug(self, title):
        """根据标题自动生成标题别名"""
        self.slug = slugify(title)

    def get_abstract(self, count, suffix='...'):
        """使用正则表达式从html中提取摘要内容"""
        plain_content = re.sub(r'<.*?>', '', self.html_content)
        abstract = ''.join(plain_content.split())[0:count]
        return abstract + suffix

    def reviewed_comments(self):
        """返回已审核通过的评论列表"""
        return [comment for comment in self.comments if comment.status == 'approved']

    @property
    def comments_count(self):
        """收到的评论总数"""
        return Comment.objects.filter(post_slug=self.slug).count()

    def clean(self):
        """保存到数据库前更新时间戳, 生成标题别名并将markdown文本转换为html"""
        now = datetime.utcnow()
        if not self.pub_time:
            self.pub_time = now
        self.update_time = now
        if not self.slug:
            self.set_slug(self.title)

        self.html_content = markdown2.markdown(self.raw_content,
                                               extras=['code-friendly', 'fenced-code-blocks', 'tables'])
        self.html_content = get_clean_html_content(self.html_content)
        # 若未设置摘要，自动截取正文作为摘要
        if not self.abstract:
            self.abstract = self.get_abstract(140)

    def to_dict(self):
        """把类的对象转化为 dict 类型的数据，将对象序列化"""
        post_dict = {
            'title': self.title,
            'slug': self.slug,
            'abstract': self.abstarct,
            'author': self.author,
            'html_content': self.html_content,
            'raw_content': self.raw_content,
            'pub_time': self.pub_time,
            'update_time': self.update_time,
            'category': self.category,
            'tags': self.tags,
            'weight': self.weight,
            'can_comment': self.can_comment,
            'from_admin': self.from_admin,
            'type': self.type,
        }

        return post_dict

    meta = {
        'indexes': ['slug', 'type'],  # 添加type索引以加快对专用页面的查询速度
        'ordering': ['-pub_time']
    }


class Comment(db.Document):
    """定义评论的数据模型"""
    author = db.StringField(max_length=30, required=True)
    email = db.EmailField(max_length=255, required=True)
    homepage = db.URLField(max_length=255)
    post_slug = db.StringField(required=True)
    post_title = db.StringField(default='default article')
    md_content = db.StringField(required=True)
    html_content = db.StringField(required=True)
    pub_time = db.DateTimeField()
    reply_to = db.ReferenceField('self')
    status = db.StringField(choices=COMMENT_STATUS, default='pending')
    from_post_author = db.BooleanField(default=False)
    from_admin = db.BooleanField(default=False)
    gravatar_id = db.StringField(default='00000000000')

    def clean(self):
        """保存到数据库前更新时间戳,生成头像id，并将markdown文本转换为html"""
        html_content = markdown2.markdown(self.md_content,
                                          extras=['code-friendly', 'fenced-code-blocks', 'tables', 'nofollow'])
        self.html_content = get_clean_html_content(html_content)

        if not self.pub_time:
            self.pub_time = datetime.utcnow()

        # 根据邮箱签名生成头像，若无邮箱则使用默认头像
        if self.email:
            self.gravatar_id = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def get_avatar_url(self, base_url=GRAVATAR_CDN_BASE, img_size=44, default_img_url=GRAVATAR_DEFAULT_IMAGE):
        """通过 gavatar_id 从cdn 获取头像图片的链接。

        获取时可传入大小和默认图片参数
        :param base_url: cdn地址
        :param img_size: 需要的图片大小,默认为44
        :param default_img_url: 没有匹配头像时的默认图片
        :return: 图片url
        """
        gravatar_url = base_url + self.gravatar_id
        params = {}
        if img_size:
            params['s'] = str(img_size)
        if default_img_url:
            params['d'] = default_img_url
        if params:
            gravatar_url = '{0}?{1}'.format(gravatar_url, urlencode(params))
        return gravatar_url

    meta = {
        'ordering': ['-update_time']
    }


class PostStatistic(db.Document):
    """统计每篇文章的阅读次数等统计信息"""
    post = db.ReferenceField(Post, reverse_delete_rule=db.CASCADE)  # 与文章级联删除
    visit_count = db.IntField(default=0)
    verbose_count_base = db.IntField(default=0)
    post_type = db.StringField(max_length=64, default='post')


class Tracker(db.Document):
    """记录访客信息"""
    post = db.ReferenceField(Post, reverse_delete_rule=db.CASCADE)  # 与文章级联删除
    ip = db.StringField()
    user_agent = db.StringField()
    create_time = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'ordering': ['-create_time']
    }


class Widget(db.Document):
    """在主页显示文本内容的widget"""
    title = db.StringField(default='widget')
    raw_content = db.StringField()
    html_content = db.StringField()
    priority = db.IntField(default=10000)
    pub_time = db.DateTimeField()

    def clean(self):
        """保存到数据库前更新时间戳,生成头像id，并将markdown文本转换为html"""
        if self.raw_content:
            self.html_content = markdown2.markdown(self.raw_content,
                                                   extras=['code-friendly', 'fenced-code-blocks', 'tables'])
        self.html_content = get_clean_html_content(self.html_content)

        if not self.pub_time:
            self.pub_time = datetime.utcnow()

    meta = {
        'ordering': ['priority']
    }
