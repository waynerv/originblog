from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, \
    HiddenField
from wtforms.validators import DataRequired, Length, Email, URL, Optional


class CommentForm(FlaskForm):
    """定义评论表单"""
    author = StringField('* Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('* Email', validators=[DataRequired(), Email(), Length(1, 254)])
    homepage = StringField('Homepage', validators=[Optional(), URL(), Length(0, 255)])
    content = TextAreaField('* Comment <span class="badge badge-info">markdown</span>',
                            validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserCommentForm(FlaskForm):
    """定义已登录用户的评论表单"""
    author = HiddenField('* Name', validators=[DataRequired(), Length(1, 30)])
    email = HiddenField('* Email', validators=[DataRequired(), Email(), Length(1, 254)])
    homepage = HiddenField('Homepage', validators=[Optional(), URL(), Length(0, 255)])
    content = TextAreaField('* Comment <small><span class="badge badge-info">markdown</span></small>',
                            validators=[DataRequired()])
    submit = SubmitField('Submit')
