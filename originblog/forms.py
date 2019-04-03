from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, \
    HiddenField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, URL, Optional, Regexp, EqualTo

from originblog.models import Draft, Post, User
from originblog.settings import BlogSettings

ROLES = [(i, i) for i in BlogSettings.ROLE_PERMISSION_MAP]


class LoginForm(FlaskForm):
    """定义登录表单"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    """定义注册表单"""
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 20),
        Regexp('^[a-zA-Z0-9]*$', message='The username should contain only a-z, A-Z, 0-9.')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 255), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128),
                                                     EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(field):
        """验证用户名是否已注册"""
        if User.objects.filter(User.username == field.data).first():
            raise ValidationError('The username is already in use.')

    @staticmethod
    def validate_email(field):
        """验证email是否已注册"""
        if User.objects.filter(User.email == field.data.lower()).first():
            raise ValidationError('The email is already in use.')


class SuUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 255), Email()])
    is_superuser = BooleanField('Is superuser')
    is_email_confirmed = BooleanField('Is Email confirmed.')
    role = SelectField('Role', choices=ROLES)
    name = StringField('Display Name', validators=[Length(1, 128)])
    bio = StringField('Bio', validators=[Optional(), Length(0, 200)])
    homepage_url = StringField('Homepage', validators=[Optional(), URL()])
    weibo = StringField('Weibo', validators=[Optional(), URL()])
    weixin = StringField('Weixin', validators=[Optional(), URL()])
    github = StringField('github', validators=[Optional(), URL()])


class ProfileForm(FlaskForm):
    """定义修改个人资料表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 255), Email()])
    name = StringField('Display Name', validators=[Length(1, 128)])
    bio = StringField('Bio', validators=[Optional(), Length(0, 200)])
    homepage_url = StringField('Homepage', validators=[Optional(), URL()])
    weibo = StringField('Weibo', validators=[Optional(), URL()])
    weixin = StringField('Weixin', validators=[Optional(), URL()])
    github = StringField('github', validators=[Optional(), URL()])

    @staticmethod
    def validate_username(field):
        """验证用户名是否已注册"""
        if User.objects.filter(User.username == field.data).first():
            raise ValidationError('The username is already in use.')

    @staticmethod
    def validate_email(field):
        """验证email是否已注册"""
        if User.objects.filter(User.email == field.data.lower()).first():
            raise ValidationError('The email is already in use.')


class ForgetPasswordForm(FlaskForm):
    """定义忘记密码表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 255), Email()])
    submit = SubmitField()


class ResetPasswordForm(FlaskForm):
    """定义忘记密码后重设密码表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 255), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField()


class ChangePasswordForm(FlaskForm):
    """定义修改密码表单"""
    current_password = PasswordField('Current password', validators=[DataRequired(), Length(6, 128)])
    password = PasswordField('New password', validators=[DataRequired(), Length(6, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    """定义文章编辑表单"""
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    # TODO slug = StringField('Slug', validators=[DataRequired(), Length(1, 255)])
    weight = IntegerField('Weight', default=10)
    raw_content = TextAreaField('Content', validators=[DataRequired()])
    abstract = TextAreaField('Abstract', validators=[Optional(), Length(0, 255)])
    category = StringField('Category', validators=[Optional(), Length(0, 64)])
    tags = StringField('Tags(separate with space)', validators=[Optional(), Length(0, 64)])
    post_id = HiddenField('post_id')
    from_draft = HiddenField('from_draft')
    submit = SubmitField('Submit')

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.category.choices = [(category.id, category.name)
    #                              for category in Category.query.order_by(Category.name).all()]

    def validate_slug(self, field):
        """验证是否有已重复的slug"""
        if self.from_draft.data and self.from_draft.data == 'true':
            posts = Draft.objects.filter(slug=field.data)
        else:
            posts = Post.objects.filter(slug=field.data)
        if posts.count() > 0:
            if not self.post_id.data or str(posts[0].id) != self.post_id.data:
                raise ValidationError('slug already in use')


SuPostForm = model_form(Post, exclude=['pub_time', 'update_time', 'html_content', 'category', 'tags'])


class CommentForm(FlaskForm):
    """定义评论表单"""
    author = StringField('* Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('* Email', validators=[DataRequired(), Email(), Length(1, 254)])
    homepage = StringField('Homepage', validators=[Optional(), URL(), Length(0, 255)])
    content = TextAreaField('* Comment <small><span class="label label-info">markdown</span></small>',
                            validators=[DataRequired()])
    comment_id = HiddenField('comment_id')
    submit = SubmitField('Submit')


class UserCommentForm(FlaskForm):
    """定义已登录用户的评论表单"""
    author = HiddenField('* Name', validators=[DataRequired(), Length(1, 30)])
    email = HiddenField('* Email', validators=[DataRequired(), Email(), Length(1, 254)])
    homepage = HiddenField('Homepage', validators=[Optional(), URL(), Length(0, 255)])
    content = TextAreaField('* Comment <small><span class="label label-info">markdown</span></small>',
                            validators=[DataRequired()])
    comment_id = HiddenField('comment_id')
    submit = SubmitField('Submit')


class SessionCommentForm(FlaskForm):
    email = HiddenField('* Email')
    author = HiddenField('* Name')
    homepage = HiddenField('Homepage')
    content = TextAreaField('* Comment', validators=[DataRequired()])
    comment_id = HiddenField('comment_id')


class AboutForm(FlaskForm):
    blog_title = StringField('Blog title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Subtitle', validators=[DataRequired(), Length(1, 100)])
    about = TextAreaField('About', validators=[DataRequired()])
    submit = SubmitField('Submit')


class WidgetForm(FlaskForm):
    """定义首页组件表单"""
    title = StringField('Title', validators=[DataRequired(), Length(1, 20)])
    content = StringField('Content', validators=[DataRequired(), URL(), Length(1, 255)])
    content_type = RadioField('Content Type', choices=[('markdown', 'markdown'), ('html', 'html')], default='html')
    priority = IntegerField(default=10000)
    submit = SubmitField('Submit')
