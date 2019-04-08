from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, ValidationError, TextAreaField, \
    IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, URL, Optional

from originblog.models import Post, User
from originblog.settings import BlogSettings

ROLES = [(i, i) for i in BlogSettings.ROLE_PERMISSION_MAP]


class MetaUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 255), Email()])
    # is_superuser = BooleanField('Is superuser')
    email_confirmed = BooleanField('Is Email confirmed.')
    role = SelectField('Role', choices=ROLES)
    name = StringField('Display Name', validators=[Length(1, 128)])
    bio = StringField('Bio', validators=[Optional(), Length(0, 200)])
    homepage = StringField('Homepage', validators=[Optional(), URL()])
    weibo = StringField('Weibo', validators=[Optional(), URL()])
    weixin = StringField('Weixin', validators=[Optional(), URL()])
    github = StringField('github', validators=[Optional(), URL()])
    active = BooleanField('Active', default=True)

    @staticmethod
    def validate_email(field):
        """验证email是否已注册"""
        if User.objects.filter(User.email == field.data.lower()).first():
            raise ValidationError('The email is already in use.')


class PostForm(FlaskForm):
    """定义文章编辑表单"""
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    # TODO:slug = StringField('Slug', validators=[Optional(), Length(0, 230)])
    weight = IntegerField('Weight', default=10)
    raw_content = TextAreaField('Content', validators=[DataRequired()])
    abstract = TextAreaField('Abstract', validators=[Optional(), Length(0, 255)])
    category = StringField('Category', validators=[Optional(), Length(0, 64)])
    tags = StringField('Tags(separate with space)', validators=[Optional(), Length(0, 64)])
    type = RadioField('Type', choices=[('post', 'post'), ('page', 'page')], default='post')
    submit = SubmitField('Submit')

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.category.choices = [(category.id, category.name)
    #                              for category in Category.query.order_by(Category.name).all()]

    # def validate_slug(self, field):
    #     """验证是否有已重复的slug"""
    #     posts = Post.objects.filter(slug=field.data)
    #     if posts.count() > 0:
    #         if not self.post_id.data or str(posts[0].id) != self.post_id.data:
    #             raise ValidationError('slug already in use')


# 使用flask-mongoengine从模型直接生成表单
MetaPostForm = model_form(Post, exclude=['slug', 'author', 'html_content', 'update_time', 'from_admin'])


class WidgetForm(FlaskForm):
    """定义首页组件表单"""
    title = StringField('Title', validators=[DataRequired(), Length(1, 20)])
    content = StringField('Content', validators=[DataRequired(), URL(), Length(1, 255)])
    content_type = RadioField('Content Type', choices=[('markdown', 'markdown'), ('html', 'html')], default='html')
    priority = IntegerField(default=10000)
    submit = SubmitField('Submit')
