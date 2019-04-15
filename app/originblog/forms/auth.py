from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from originblog.models import User


class LoginForm(FlaskForm):
    """定义登录表单"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


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

    def validate_username(self, field):
        """验证用户名是否已注册"""
        if User.objects.filter(username=field.data).first():
            raise ValidationError('The username is already in use.')

    def validate_email(self, field):
        """验证email是否已注册"""
        if User.objects.filter(email=field.data.lower()).first():
            raise ValidationError('The email is already in use.')


class ForgetPasswordForm(FlaskForm):
    """定义忘记密码表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 255), Email()])
    submit = SubmitField('Send Email')


class ResetPasswordForm(FlaskForm):
    """定义忘记密码后重设密码表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 255), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
