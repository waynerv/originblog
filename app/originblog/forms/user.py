from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, URL, Optional, EqualTo
from flask_login import current_user

from originblog.models import User


class ChangePasswordForm(FlaskForm):
    """定义修改密码表单"""
    current_password = PasswordField('Current password', validators=[DataRequired(), Length(6, 128)])
    password = PasswordField('New password', validators=[DataRequired(), Length(6, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()


class ProfileForm(FlaskForm):
    """定义修改个人资料表单"""
    name = StringField('Name', validators=[Length(1, 128)])
    bio = StringField('Bio', validators=[Optional(), Length(0, 200)])
    homepage = StringField('Homepage', validators=[Optional(), URL()])
    weibo = StringField('Weibo', validators=[Optional(), URL()])
    weixin = StringField('Weixin', validators=[Optional(), URL()])
    github = StringField('GitHub', validators=[Optional(), URL()])
    submit = SubmitField()


class ChangeEmailForm(FlaskForm):
    email = StringField('New email', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField()

    def validate_email(self, field):
        """验证email是否已注册"""
        if User.objects.filter(email=field.data.lower()).first():
            raise ValidationError('The email is already in use.')


class DeleteAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)],
                           render_kw={'placeholder':'Please type in the username of your account to confirm.'})
    submit = SubmitField()

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('Wrong username.')
