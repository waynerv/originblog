import hashlib
import re
import urllib
from datetime import datetime

import bleach
import markdown2
from flask_login import UserMixin
from unidecode import unidecode
from werkzeug.security import generate_password_hash, check_password_hash

from originblog.extensions import db
from originblog.settings import blog_settings

COMMENT_STATUS = ('approved', 'pending', 'spam', 'deleted')
GAVATAR_CDN_BASE = blog_settings['GAVATAR_CDN_BASE']
GAVATAR_DEFAULT_IMAGE = blog_settings['gavatar_default_image']

ROLES = ('admin', 'editor', 'writer', 'reader')

# 编译分割标题获取别名的正则表达式
_punct_re = re.compile(r'[\t !"#$%&\-/<=>?@\[\\\]^_`{|},.]+')


def get_clean_html_content(html_content):
    """对转换成HTML的markdown文本进行清洗"""
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
    return unidecode(delim.join(result))


class User(db.Document, UserMixin):
    username = db.StringField(max_length=20, required=True)
    password_hash = db.StringField(max_length=128, required=True)
    name = db.StringField(max_length=20, default=username)
    email = db.EmailField(max_length=255)
    create_time = db.DateTimeField(default=datetime.utcnow, required=True)
    last_login = db.DateTimeField(default=datetime.utcnow, required=True)
    email_confirmed = db.BooleanField(default=False)
    is_superuser = db.BooleanField(default=False)
    role = db.StringField(default='reader', choices=ROLES)
    bio = db.StringField(max_length=200)
    homepage = db.URLField(max_length=255)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        try:
            return self.username
        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')


class Post(db.Document):
    """定义文章数据模型"""
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    abstract = db.StringField(max_length=255)
    author = db.ReferenceField(User)
    html_content = db.StringField(required=True)
    raw_content = db.StringField(required=True)
    pub_time = db.DateTimeField()
    update_time = db.DateTimeField()
    category = db.StringField(max_length=64, default='default')
    tags = db.ListField(db.StringField(max_length=30))
    can_comment = db.BooleanField(default=True)
    is_draft = db.BooleanField(default=False)
    weight = db.IntField(default=10)

    def set_slug(self, title):
        """根据标题自动生成标题别名"""
        self.slug = slugify(title)

    def reviewed_comments(self):
        """返回已审核通过的评论列表"""
        return [comment for comment in self.comments if comment.reviewed is True]

    def save(self, *args, **kwargs):
        """保存到数据库前更新时间戳并将markdown文本转换为html"""
        now = datetime.utcnow()
        if not self.sub_time:
            self.pub_time = now
        self.update_time = now
        self.html_content = markdown2.markdown(self.raw_content,
                                               extras=['code-friendly', 'fenced-code-blocks', 'tables'])
        self.html_content = get_clean_html_content(self.html_content)
        return super(Post, self).save(*args, **kwargs)

    # 把类的对象转化为 dict 类型的数据，将对象序列化
    def to_dict(self):
        post_dict = {}

        post_dict['title'] = self.title
        post_dict['slug'] = self.slug
        post_dict['abstract'] = self.abstarct
        post_dict['author'] = self.author
        post_dict['content_html'] = self.content
        post_dict['content_raw'] = self.raw_content
        post_dict['pub_time'] = self.pub_time
        post_dict['update_time'] = self.update_time
        post_dict['category'] = self.category
        post_dict['tags'] = self.tags
        post_dict['comments'] = self.comments
        post_dict['can_comment'] = self.can_comment

        return post_dict

    meta = {
        'indexes': ['slug'],
        'ordering': ['-pub_time']
    }


class Draft(db.Document):
    """定义草稿数据模型"""
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    abstract = db.StringField(max_length=255)
    author = db.ReferenceField(User)
    html_content = db.StringField(required=True)
    raw_content = db.StringField(required=True)
    pub_time = db.DateTimeField()
    update_time = db.DateTimeField()
    category = db.StringField(max_length=64, default='default')
    tags = db.ListField(db.StringField(max_length=30))
    is_draft = db.BooleanField(default=True)
    weight = db.IntField(default=10)

    def set_slug(self, title):
        """根据标题自动生成标题别名"""
        self.slug = slugify(title)

    def save(self, *args, **kwargs):
        """保存到数据库前更新时间戳并将markdown文本转换为html"""
        now = datetime.utcnow()
        if not self.sub_time:
            self.pub_time = now
        self.update_time = now
        self.html_content = markdown2.markdown(self.raw_content,
                                               extras=['code-friendly', 'fenced-code-blocks', 'tables'])
        self.html_content = get_clean_html_content(self.html_content)
        return super(Draft, self).save(*args, **kwargs)

    meta = {
        'indexes': ['slug'],
        'ordering': ['-update_time']
    }


class Comment(db.Document):
    author = db.StringField(max_length=20, required=True)
    email = db.EmailField(max_length=255, required=True)
    homepage = db.URLField(max_length=255)
    post_slug = db.StringField(required=True)
    post_title = db.StringField(default='default article')
    md_content = db.StringField(required=True)
    html_content = db.StringField(required=True)
    pub_time = db.DateTimeField()
    update_time = db.DateTimeField()
    reply_to = db.ReferenceField('self')
    status = db.StringField(choices=COMMENT_STATUS, default='pending')
    gavatar_id = db.StringField(default='00000000000')

    def save(self, *args, **kwargs):
        """保存到数据库前更新时间戳,生成头像id，并将markdown文本转换为html"""
        if self.md_content:
            html_content = markdown2.markdown(self.raw_content,
                                              extras=['code-friendly', 'fenced-code-blocks', 'tables', 'nofollow'])
            self.html_content = get_clean_html_content(html_content)

        if not self.pub_time:
            self.pub_time = datetime.utcnow()
        self.update_time = datetime.utcnow()

        # 根据邮箱签名生成头像，若无邮箱则使用默认头像
        if self.email:
            self.gavatar_id = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

        return super(Comment, self).save(*args, **kwargs)

    def get_avatar_url(self, base_url=GAVATAR_CDN_BASE, img_size=0, default_img_url=None):
        gavatar_url = base_url + self.gavatar_id
        params = {}
        if img_size:
            params['s'] = str(img_size)
        if default_img_url:
            params['d'] = default_img_url
        if params:
            gavatar_url = '{0}?{1}'.format(gavatar_url, urllib.urlencode(params))
        return gavatar_url

    meta = {
        'ordering': ['-update_time']
    }


class PostStatistics(db.Document):
    post = db.ReferenceField(Post)
    visit_count = db.IntField(default=0)
    verbose_count_base = db.IntField(default=0)


class Widget(db.Document):
    title = db.StringField(default='widget')
    raw_content = db.StringField()
    html_content = db.StringField()
    priority = db.IntField(default=10000)
    pub_time = db.DateTimeField()

    def save(self, *args, **kwargs):
        if self.raw_content:
            self.html_content = markdown2.markdown(self.raw_content,
                                                   extras=['code-friendly', 'fenced-code-blocks', 'tables'])
        self.html_content = get_clean_html_content(self.html_content)

        if not self.pub_time:
            self.pub_time = datetime.utcnow()

        return super(Widget, self).save(*args, **kwargs)

    meta = {
        'ordering': ['priority']
    }
