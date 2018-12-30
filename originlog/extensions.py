from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment

db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()