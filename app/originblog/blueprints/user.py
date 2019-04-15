from flask import Blueprint, render_template, url_for, request, flash, redirect, current_app
from flask_login import login_required, fresh_login_required, current_user

from originblog.emails import send_change_email_email
from originblog.forms.user import ProfileForm, ChangePasswordForm, ChangeEmailForm, DeleteAccountForm
from originblog.models import User, Post
from originblog.settings import Operations

user_bp = Blueprint('user', __name__)


@user_bp.route('/<username>')
def index(username):
    """显示用户主页"""
    user = User.objects.get_or_404(username=username)
    posts = Post.objects.filter(type='post', author=user).order_by('-pub_time')

    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['APP_POST_PER_PAGE']
    pagination = posts.paginate(page, per_page=per_page)
    return render_template('user/user_index.html', user=user, pagination=pagination)


@user_bp.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑用户个人资料"""
    form = ProfileForm()

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.homepage = form.homepage.data
        current_user.bio = form.bio.data
        current_user.social_networks['weibo']['url'] = form.weibo.data
        current_user.social_networks['weixin']['url'] = form.weixin.data
        current_user.social_networks['github']['url'] = form.github.data
        current_user.save()
        flash('Profile updated.', 'success')
        return redirect(url_for('user.edit_profile'))
    form.name.data = current_user.name
    form.homepage.data = current_user.homepage
    form.bio.data = current_user.bio
    form.weibo.data = current_user.social_networks['weibo'].get('url')
    form.weixin.data = current_user.social_networks['weixin'].get('url')
    form.github.data = current_user.social_networks['github'].get('url')
    return render_template('user/edit_profile.html', form=form)


@user_bp.route('/settings/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """更改密码"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.validate_password(form.old_password.data):
            current_user.set_password(form.password.data)
            current_user.save()
            flash('Password updated.', 'success')
            return redirect(url_for('user.index', username=current_user.username))
        else:
            flash('Old password is incorrect.', 'warning')
    return render_template('user/change_password.html', form=form)


@user_bp.route('/settings/change-email', methods=['GET', 'POST'])
@fresh_login_required
def change_email_request():
    """发送更改邮箱令牌"""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data.lower()
        token = current_user.generate_token(operation=Operations.CHANGE_EMAIL, new_email=new_email)
        send_change_email_email(user=current_user, token=token, to=new_email)
        flash('Confirm email sent, check your inbox.', 'info')
        return redirect(url_for('user.index', username=current_user.username))
    return render_template('user/change_email.html', form=form)


@user_bp.route('/change-email/confirm/<token>')
@login_required
def change_email(token):
    """验证令牌，修改邮箱"""
    if current_user.validate_token(token=token, operation=Operations.CHANGE_EMAIL):
        flash('Email updated.', 'success')
        return redirect(url_for('user.index', username=current_user.username))
    else:
        flash('Invalid or expired token.', 'warning')
        return redirect(url_for('user.change_email_request'))


@user_bp.route('/settings/delete-account', methods=['GET', 'POST'])
@fresh_login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        current_user.delete()
        flash('Account deleted permanently, goodbye!', 'success')
        return redirect(url_for('blog.index'))
    return render_template('user/delete_account.html', form=form)