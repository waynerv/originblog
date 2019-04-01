from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_mongoengine import MongoEngine
from flask_wtf import CSRFProtect

db = MongoEngine()
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = '请先登录！'


@login_manager.user_loader
def load_user(username):
    """
    使用Flask Login 必须创建一个user_loader回调函数来根据session中取回的user ID（unicode） 取得user对象，否则返回None
    It should return None (not raise an exception) if the ID is not valid.
     (In that case, the ID will manually be removed from the session and processing will continue.)
    :param username:
    :return:
    """
    from originblog.models import User
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExists:
        user = None
    return user
