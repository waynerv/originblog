import os

from flask import Flask, render_template

from originlog.blueprints.admin import admin_bp
from originlog.blueprints.auth import auth_bp
from originlog.blueprints.blog import blog_bp
from originlog.commands import register_command
from originlog.extensions import db, ckeditor, mail, moment
from originlog.models import Admin, Category
from originlog.settings import config


def create_app():
    app = Flask('originlog')
    config_name = os.getenv('FLASK_CONFIG', 'development')
    app.config.from_object(config[config_name])

    register_blueprints(app)

    register_extensions(app)

    register_command(app)

    register_template_context(app)

    register_error_handler(app)

    return app


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_extensions(app):
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


def register_error_handler(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def bad_request(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def bad_request(e):
        return render_template('errors/500.html'), 500
