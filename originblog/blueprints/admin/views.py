from flask import Blueprint, render_template

from originblog.blueprints.admin.api import AdminIndex, Posts, PostItem, MetaPosts, MetaPostItem, Comments, \
    CommentItem, Users, MetaUserItem, Widgets, WidgetItem, PostStatistics, PostStatisticItem
from originblog.decorator import admin_required, permission_required
from originblog.forms.admin import PostForm, WidgetForm, MetaPostForm
from originblog.forms.auth import RegisterForm

admin_bp = Blueprint('admin', __name__)

# 注册路由
admin_bp.add_url_rule('/', view_func=AdminIndex.as_view('index'), methods=['GET'])

admin_bp.add_url_rule('/posts', view_func=Posts.as_view('posts'), methods=['GET', 'POST'])
admin_bp.add_url_rule('/posts/<slug>', view_func=PostItem.as_view('post'), methods=['GET', 'POST', 'PATCH', 'DELETE'])

admin_bp.add_url_rule('/pages', view_func=Posts.as_view('pages'), methods=['GET', 'POST'],
                      defaults={'post_type': 'page'})
admin_bp.add_url_rule('/pages/<slug>', view_func=PostItem.as_view('page'), methods=['GET', 'POST', 'PATCH', 'DELETE'])

admin_bp.add_url_rule('/meta/posts', view_func=MetaPosts.as_view('meta_posts'), methods=['GET', 'POST'])
admin_bp.add_url_rule('/meta/posts/<slug>', view_func=MetaPostItem.as_view('meta_post'), methods=['GET', 'POST'])

admin_bp.add_url_rule('/posts/comments', view_func=Comments.as_view('comments'), methods=['GET', 'DELETE'])
admin_bp.add_url_rule('/posts/comments/<pk>', view_func=CommentItem.as_view('comment'), methods=['PATCH', 'DELETE'])

admin_bp.add_url_rule('/users', view_func=Users.as_view('users'), methods=['GET', 'POST'])
admin_bp.add_url_rule('/meta/users/<pk>', view_func=MetaUserItem.as_view('meta_user'),
                      methods=['GET', 'POST', 'DELETE'])

admin_bp.add_url_rule('/widgets', view_func=Widgets.as_view('widgets'), methods=['GET', 'POST'])
admin_bp.add_url_rule('/widgets/<pk>', view_func=WidgetItem.as_view('widget'), methods=['GET', 'POST', 'DELETE'])

admin_bp.add_url_rule('/posts/statistics', view_func=PostStatistics.as_view('statistics'), methods=['GET'])
admin_bp.add_url_rule('/posts/statistics/<slug>', view_func=PostStatisticItem.as_view('statistic'), methods=['GET'])


@admin_bp.route('/posts/new_post')
@permission_required('POST')
def new_post():
    form = PostForm()
    form.type.data = 'post'
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/posts/add_user')
@permission_required('MODERATE')
def add_user():
    form = RegisterForm()
    return render_template('admin/new_user.html', form=form)


@admin_bp.route('/pages/new_page')
@admin_required
def new_page():
    form = PostForm()
    form.type.data = 'page'
    return render_template('admin/new_page.html', form=form)


@admin_bp.route('/widgets/new_widget')
@admin_required
def new_widget():
    form = WidgetForm()
    return render_template('admin/new_widget.html', form=form)


@admin_bp.route('/meta/posts/new_article')
@admin_required
def new_article():
    form = MetaPostForm()
    return render_template('admin/new_article.html', form=form)
