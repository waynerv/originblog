from functools import wraps

from flask import abort
from flask_login import current_user


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
    return permission_required('ADMINSTRATE')(func)
