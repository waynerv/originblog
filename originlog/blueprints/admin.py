from flask import Blueprint, request, current_app, render_template
from flask_login import login_required

from originlog.models import Post

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINLOG_MANAGE_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('admin/manage_post.html', posts=posts, pagination=pagination)


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    pass


@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    pass


@admin_bp.route('/post/new')
@login_required
def new_post():
    pass


@admin_bp.route('/post/edit')
@login_required
def edit_post():
    pass


@admin_bp.route('/post/delete')
@login_required
def delete_post():
    pass


@admin_bp.route('/category/new')
@login_required
def new_category():
    pass


@admin_bp.route('/settings')
@login_required
def settings():
    pass
