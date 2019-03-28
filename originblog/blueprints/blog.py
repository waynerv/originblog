from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, abort, make_response
from flask_login import current_user
from mongoengine.queryset.visitor import Q

from originblog.emails import send_new_comment_email
from originblog.extensions import db
from originblog.forms import CommentForm
from originblog.models import Post, Comment, Widget
from originblog.utils import redirect_back

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """查询所有已发表的文章，根据特定查询参数进行筛选分页，传入到首页模板"""

    # 获取已发表并且权重值大于0的文章的QuerySet，按权重和发表时间排序
    pub_posts = Post.objects.filter(is_draft=False).order_by('-weight', '-pub_time')
    posts = pub_posts.filter(Q(weight_gt=0) | Q(weight=None))

    # 根据查询参数获取特定分类的文章QuerySet
    category = request.args.get('categorty')
    if category:
        posts = posts.filter(category=category)

    # 根据查询参数获取特定标签的文章QuerySet
    tag = request.args.get('tag')
    if tag:
        posts = posts.filter(tags=tag)

    # 根据查询参数获取特定文本关键词的搜索结果
    keywords = request.args.get('keywords')
    if keywords:
        posts = posts.filter(Q(raw_content__icontains=keywords) | Q(title_icontains=keywords))

    # 获取首页所有组件对象
    widgets = Widget.objects

    # 从查询参数获取当前页数并对QuerySet分页，页数默认值为1
    page = request.args.get('page', default=1, type=int)  # 从查询字符串获取当前页数
    per_page = current_app.config['ORIGINLOG_POST_PER_PAGE']  # 每页数量
    pagination = posts.paginate(page, per_page=per_page)  # 分页对象
    return render_template('blog/index.html', pagination=pagination, tags=tags, widgets=widgets)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'Post'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['ORIGINLOG_ADMIN_EMAIL']
        form.site.data = url_for('blog.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(author=author, email=email, site=site, body=body, from_admin=from_admin, reviewed=reviewed,
                          post=post)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_comment_email(replied_comment)  # 是否审核通过后再通知被回复用户比较合适？

        db.session.add(comment)
        db.session.commit()
        flash('Thanks, your comment will be published after reviewed.', 'info')
        send_new_comment_email(post)
        return redirect(url_for('blog.show_post', post_id=post_id))

    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINLOG_POST_PER_PAGE']
    pagination = Comment.query.filter(Comment.post_id == post_id).filter(Comment.reviewed == True).order_by(
        Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINLOG_POST_PER_PAGE']
    pagination = Post.query.filter(Post.category_id == category_id).order_by(
        Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.post.can_comment:
        return redirect(
            url_for('blog.show_post', post_id=comment.post.id, reply=comment_id, author=comment.author) + '#comment-form')
    else:
        flash('This post is comment disabled.', 'warning')
        return redirect_back()


@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['ORIGINLOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response
