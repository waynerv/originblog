from flask_bootstrap import Bootstrap
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_moment import Moment
from flask_mongoengine import MongoEngine
from flask_wtf import CSRFProtect
from mongoengine import DoesNotExist

db = MongoEngine()
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(username):
    """
        使用Flask Login 必须创建一个user_loader回调函数来根据session中取回的user ID（unicode） 取得user对象，ID 无效应返回None
        :param username: unicode ID
        :return: 用户对象或None
        """
    from originblog.models import User
    try:
        user = User.objects.get(username=username)
    except DoesNotExist:
        user = None
    return user


class Guest(AnonymousUserMixin):
    """为匿名用户创建专门的类，以便实现对角色和权限的检验"""

    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
        return False


login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录！'
login_manager.login_message_category = 'warning'
login_manager.refresh_view = 'auth.re_authenticate'
login_manager.needs_refresh_message = '请重新认证！'
login_manager.needs_refresh_message_category = 'warning'
login_manager.anonymous_user = Guest
