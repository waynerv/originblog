from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user

from originblog.forms import LoginForm, RegisterForm
from originblog.models import User
from originblog.utils import redirect_back
from originblog.settings import Operations
from originblog.emails import send_confirm_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """处理用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = User.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """处理用户注销"""
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()


@auth_bp.route('/register')
def register():
    """处理用户注册"""
    if current_user.is_authenticated:
        redirect(url_for('blog.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(name=name, username=username, email=email)
        user.set_password(password)
        user.save()

        token = user.generate_token(Operations.CONFIRM)
        send_confirm_email(user=user, token=token)
        flash('Confirm email sent, check your inbox.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)



