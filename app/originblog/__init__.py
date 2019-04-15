import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from originblog.blueprints.admin.views import admin_bp
from originblog.blueprints.auth import auth_bp
from originblog.blueprints.blog import blog_bp
from originblog.blueprints.user import user_bp
from originblog.commands import register_command
from originblog.extensions import db, mail, moment, bootstrap, login_manager, csrf
from originblog.models import User, Comment, Post
from originblog.settings import config, BlogSettings


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('originblog')
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
    app.register_blueprint(user_bp, url_prefix='/user')


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.can('MODERATE'):
            unread_comments = Comment.objects.filter(status='pending').count()
        else:
            unread_comments = 0

        blog_meta = BlogSettings.BLOG_META
        # 获取所有文章的标签列表
        tags = Post.objects.distinct('tags')
        # 通过聚集查询获取所有文章的分类以及对应的文章数量
        categories = Post.objects.aggregate(
            {'$group':{
                '_id':{'category': '$category'},
                'name':{'$first': '$category'},
                'count':{'$sum': 1}
            }}
        )
        return dict(unread_comments=unread_comments, tags=tags, categories=categories, blog_meta=blog_meta)


def register_error_handler(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(401)
    def bad_request(e):
        return render_template('errors/401.html'), 401

    @app.errorhandler(CSRFError)
    def bad_request(e):
        return render_template('errors/400.html', description=e.description), 400

    @app.errorhandler(403)
    def page_not_find(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_find(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def bad_request(e):
        return render_template('errors/500.html'), 500


def register_logger(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler('log/originblog.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)
