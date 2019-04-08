from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user, login_fresh, confirm_login

from originblog.forms.auth import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm
from originblog.models import User
from originblog.utils import redirect_back
from originblog.settings import Operations
from originblog.emails import send_confirm_email, send_reset_password_email

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
        email = form.email.data.lower()
        password = form.password.data
        user = User(
            name=name,
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        token = user.generate_token(Operations.CONFIRM)
        send_confirm_email(user=user, token=token)
        flash('Confirm email sent, check your inbox.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    """通过令牌确认账户"""
    if current_user.confirmed:
        return redirect(url_for('blog.index'))

    if current_user.validate_token(token, Operations.CONFIRM):
        flash('Account confirmed.', 'info')
        return redirect(url_for('blog.index'))
    else:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.resend_confirm_email'))


@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    """重新生成令牌并发送邮件"""
    if current_user.confirmed:
        return redirect(url_for('blog.index'))

    token = current_user.generate_token(Operations.CONFIRM)
    send_confirm_email(user=current_user, token=token)
    flash('New email sent, check your inbox.', 'info')
    return redirect(url_for('blog.index'))


@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    """忘记密码时发送令牌重置密码"""
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = ForgetPasswordForm()
    if form.validate_on_submit():
        email = form.data.email
        user = User.objects.filter(email=email).first()

        if user:
            token = user.generate_token(Operations.RESET_PASSWORD)
            send_reset_password_email(user=user, token=token)
            flash('Password reset email sent, check your inbox.', 'info')
            return redirect(url_for('auth.login'))
        flash('Invalid email.', 'warning')
        return redirect(url_for('auth.forget_password'))
    return render_template('auth/forget_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """填写新密码，验证令牌并修改密码"""
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.objects.filter(email=email).first()
        if user is None:
            return redirect(url_for('blog.index'))
        if user.validate_token(token, Operations.RESET_PASSWORD, password):  # 在验证令牌方法中修改密码
            flash('Password updated.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid or expired token.', 'danger')
            return redirect(url_for('auth.forget_password'))
    return render_template('auth/reset_password.html')


@auth_bp.route('re-authenticate', methods=['GET', 'POST'])
@login_required
def re_authenticate():
    """处理非新鲜登录的重认证"""
    if login_fresh():
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit() and current_user.validate_password(form.password.data):
        confirm_login()
        return redirect_back()
    return render_template('auth/login.html', form=form)
