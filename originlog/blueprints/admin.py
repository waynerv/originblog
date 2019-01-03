from flask import Blueprint, request, current_app, render_template, flash, redirect, url_for
from flask_login import login_required

from originlog.extensions import db
from originlog.forms import PostForm
from originlog.models import Post
from originlog.utils import redirect_back

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


@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category_id = form.category.data
        # category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category_id=category_id)
        post.set_slug(title)
        db.session.add(post)
        db.session.commit()
        flash('Post published.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category_id = form.category.data
        # category = Category.query.get(form.category.data)
        post.set_slug(form.title.data)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect_back()


@admin_bp.route('/category/new')
@login_required
def new_category():
    pass


@admin_bp.route('/settings')
@login_required
def settings():
    pass
