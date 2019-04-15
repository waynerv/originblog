from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, ValidationError, TextAreaField, \
    IntegerField, RadioField, SelectField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, Length, Email, URL, Optional, Regexp

from originblog.models import Post, User
from originblog.settings import BlogSettings

ROLES = [(i, i) for i in BlogSettings.ROLE_PERMISSION_MAP]


class MetaUserForm(FlaskForm):
    username = StringField('* Username', validators=[DataRequired(), Length(1, 20),
        Regexp('^[a-zA-Z0-9]*$', message='The username should contain only a-z, A-Z, 0-9.')])
    email = StringField('* Email', validators=[DataRequired(), Length(1, 255), Email()])
    email_confirmed = BooleanField('Is Email confirmed.')
    role = SelectField('Role', choices=ROLES)
    name = StringField('Name', validators=[Length(1, 128)])
    bio = StringField('Bio', validators=[Optional(), Length(0, 200)])
    homepage = StringField('Homepage', validators=[Optional(), URL()])
    weibo = StringField('Weibo', validators=[Optional(), URL()])
    weixin = StringField('Weixin', validators=[Optional(), URL()])
    github = StringField('github', validators=[Optional(), URL()])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        """覆盖构造方法，传入user对象以供验证方法调用"""
        super(MetaUserForm, self).__init__(*args, **kwargs)
        # self.role.choices = [(role.id, role.role_name) for role in Role.objects.order_by(role_name)]
        self.user = user

    def validate_username(self, field):
        """验证用户名是否已注册"""
        if field.data != self.user.username and User.objects.filter(username=field.data).first():
            raise ValidationError('The username is already in use.')

    def validate_email(self, field):
        """验证email是否已注册"""
        if field.data != self.user.email and User.objects.filter(email=field.data.lower()).first():
            raise ValidationError('The email is already in use.')


class PostForm(FlaskForm):
    """定义文章编辑表单"""
    title = StringField('* Title', validators=[DataRequired(), Length(1, 60)])
    weight = IntegerField('Weight', default=10)
    raw_content = TextAreaField('* Content', validators=[DataRequired()])
    abstract = TextAreaField('Abstract', validators=[Optional(), Length(0, 255)])
    category = StringField('Category', validators=[Optional(), Length(0, 64)])
    tags = StringField('Tags(separate with space)', validators=[Optional(), Length(0, 64)])
    type = HiddenField(default='post')
    submit = SubmitField('Submit')

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.category.choices = [(category.id, category.name)
    #                              for category in Category.query.order_by(Category.name).all()]


# 使用flask-mongoengine从模型直接生成表单
# MetaPostForm = model_form(Post, exclude=['slug', 'author', 'html_content', 'update_time', 'from_admin'])
class MetaPostForm(PostForm):
    slug = StringField('Slug', validators=[Optional(), Length(0, 250),
        Regexp('^[-a-z0-9]*$', message='The slug should contain only a-z, dash, 0-9.')])
    pub_time = DateTimeField('* Publish Time', validators=[DataRequired()])
    can_comment = BooleanField('Can Comment', default=True)
    type = RadioField('Type', choices=[('post', 'post'), ('page', 'page')], default='post')

    def validate_slug(self, field):
        """验证是否有已重复的slug"""
        posts = Post.objects.filter(slug=field.data)
        if posts.count() > 0:
            if not self.post_id.data or str(posts[0].id) != self.post_id.data:
                raise ValidationError('slug already in use')


class WidgetForm(FlaskForm):
    """定义首页组件表单"""
    title = StringField('* Title', validators=[DataRequired(), Length(1, 64)])
    content = TextAreaField('* Content', validators=[DataRequired(), Length(1, 255)])
    content_type = RadioField('Content Type', choices=[('markdown', 'markdown'), ('html', 'html')], default='markdown')
    priority = IntegerField(default=10000)
    submit = SubmitField('Submit')
