from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = '请先登录！'


@login_manager.user_loader
def load_user(user_id):
    from originlog.models import Admin
    user = Admin.query.get(int(user_id))
    return user
