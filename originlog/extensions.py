from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mail import Mail

db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()