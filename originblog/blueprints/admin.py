from flask import Blueprint, request, current_app, render_template, flash, redirect, url_for
from flask_login import login_required

from originblog.extensions import db
from originblog.forms import PostForm, CategoryForm, AboutForm, LinkForm
from originblog.models import Post, Comment, Category, Admin, Link
from originblog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINLOG_MANAGE_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('admin/manage_post.html', posts=posts, pagination=pagination)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        body_md = form.body.data
        body_html = request.form.get('flask-editormd-html-code')
        category_id = form.category.data
        # category = Category.query.get(form.category.data)
        post = Post(title=title, body_md=body_md,body_html=body_html, category_id=category_id)
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
        post.body_md = form.body.data
        post.body_html = request.form.get('flask-editormd-html-code')
        post.category_id = form.category.data
        # category = Category.query.get(form.category.data)
        post.set_slug(form.title.data)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body_md
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


@admin_bp.route('/post/set-comment/<int:post_id>', methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('Comment disabled.', 'success')
    else:
        post.can_comment = True
        flash('Comment enabled.', 'success')
    db.session.commit()
    return redirect_back()


@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all')
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINLOG_MANAGE_COMMENT_PER_PAGE']

    if filter_rule == 'all':
        filter_comments = Comment.query
    elif filter_rule == 'unread':
        filter_comments = Comment.query.filter(Comment.reviewed == False)
    elif filter_rule == 'admin':
        filter_comments = Comment.query.filter(Comment.from_admin == True)

    pagination = filter_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


@admin_bp.route('/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()


@admin_bp.route('/comment/approve/<int:comment_id>', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment approved.', 'success')
    return redirect_back()


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINLOG_MANAGE_CATEGORY_PER_PAGE']
    pagination = Category.query.order_by(Category.id).paginate(page, per_page)
    categories = pagination.items
    return render_template('admin/manage_category.html', categories=categories, pagination=pagination)


@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Category created.', 'success')
        return redirect(url_for('admin.manage_category'))
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)

    if category.name == 'default':
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('blog.index'))

    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('admin.manage_category'))
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.name == 'default':
        flash('Sorry, you can not delete default category', 'warning')
        return redirect(url_for('blog.index'))
    category.delete()
    flash('Category deleted.', 'success')
    return redirect_back()


@admin_bp.route('/link/manage')
@login_required
def manage_link():
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINLOG_MANAGE_LINK_PER_PAGE']
    pagination = Link.query.order_by(Link.id).paginate(page, per_page)
    links = pagination.items
    return render_template('admin/manage_link.html', links=links, pagination=pagination)


@admin_bp.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = LinkForm()

    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        link = Link(name=name, url=url)
        db.session.add(link)
        db.session.commit()
        flash('Link created.', 'success')
        return redirect(url_for('admin.manage_link'))
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/edit/<int:link_id>', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)

    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash('Link updated.', 'success')
        return redirect(url_for('admin.manage_link'))
    form.name.data = link.name
    form.url.data = link.url
    return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/link/delete/<int:link_id>', methods=['POST'])
@login_required
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    flash('Link deleted.', 'success')
    return redirect_back()


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = AboutForm()
    admin = Admin.query.first_or_404()

    if form.validate_on_submit():
        admin.blog_title = form.blog_title.data
        admin.blog_sub_title = form.blog_sub_title.data
        admin.about = form.about.data
        db.session.commit()
        flash('Settings updated.', 'success')
        return redirect(url_for('blog.index'))

    form.blog_title.data = admin.blog_title
    form.blog_sub_title.data = admin.blog_sub_title
    form.about.data = admin.about
    return render_template('admin/edit_about.html', form=form)

