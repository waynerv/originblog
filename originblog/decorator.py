from functools import wraps

from flask import abort, flash, url_for, Markup
from flask_login import current_user

from originblog.utils import redirect_back


def permission_required(permission):
    """检查访问视图的用户是否拥有指定权限，若无则报403错误"""

    def decorator(view):
        @wraps(view)
        def wrapped_func(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return view(*args, **kwargs)

        return wrapped_func

    return decorator


def admin_required(func):
    """检查访问视图的用户是否拥有管理员权限"""
    return permission_required('ADMINISTRATE')(func)


def confirm_required(view):
    """检查访问视图的用户是否已确认账户"""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not current_user.email_confirmed:
            message = Markup(
                'Please confirm your account first.'
                'Not receive the email?'
                '<a class="alert-link" href="%s">Resend Confirm Email</a>' % url_for('auth.resend_confirm_email')
            )
            flash(message, 'warning')
            return redirect_back()
        return view(*args, **kwargs)

    return wrapped_view
