import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from originlog.blueprints.admin import admin_bp
from originlog.blueprints.auth import auth_bp
from originlog.blueprints.blog import blog_bp
from originlog.commands import register_command
from originlog.extensions import db, ckeditor, mail, moment, bootstrap, login_manager, csrf, migrate
from originlog.models import Admin, Category, Comment, Link
from originlog.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('originlog')
    app.config.from_object(config[config_name])

    register_blueprints(app)

    register_extensions(app)

    register_command(app)

    register_template_context(app)

    register_error_handler(app)

    register_logger(app)

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
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.id).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter(Comment.reviewed == False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, unread_comments=unread_comments, links=links)


def register_error_handler(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(CSRFError)
    def bad_request(e):
        return render_template('errors/400.html', description=e.description), 400

    @app.errorhandler(404)
    def bad_request(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def bad_request(e):
        return render_template('errors/500.html'), 500


def register_logger(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler('log/originlog.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)
