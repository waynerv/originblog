from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, make_response
from flask_login import current_user
from mongoengine.queryset.visitor import Q

from originblog.forms import CommentForm, UserCommentForm
from originblog.models import Post, Comment, Widget, User
from originblog.utils import redirect_back

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """查询所有已发表的文章，根据特定查询参数进行筛选分页，传入到首页模板"""

    # 获取已发表并且权重值大于0的文章的QuerySet，按权重和发表时间排序
    pub_posts = Post.objects.filter(is_draft=False).order_by('-weight', '-pub_time')
    posts = pub_posts.filter(Q(weight__gt=0) | Q(weight=None))

    # 根据查询参数获取特定分类的文章QuerySet
    category = request.args.get('category')
    if category:
        posts = posts.filter(category=category)

    # 根据查询参数获取特定标签的文章QuerySet
    tag = request.args.get('tag')
    if tag:
        posts = posts.filter(tags=tag)

    # 根据查询参数获取特定文本关键词的搜索结果
    keywords = request.args.get('keywords')
    if keywords:
        posts = posts.filter(Q(raw_content__icontains=keywords) | Q(title__icontains=keywords))

    # 获取首页所有组件对象
    widgets = Widget.objects

    # 从查询参数获取当前页数并对QuerySet分页，页数默认值为1
    page = request.args.get('page', default=1, type=int)  # 从查询字符串获取当前页数
    per_page = current_app.config['ORIGINBLOG_POST_PER_PAGE']  # 每页数量
    pagination = posts.paginate(page, per_page=per_page)  # 分页对象

    return render_template('blog/index.html', pagination=pagination, widgets=widgets, cur_category=category,
                           cur_tag=tag, cur_keywords=keywords)


@blog_bp.route('/post/<string:slug>', methods=['GET', 'Post'])
def show_post(slug):
    """显示文章正文、评论列表与评论表单并处理表单提交。

    已登录用户不需要手动填写评论表单的个人信息,通过查询参数reply-to判断是否为评论回复，并进行相应处理
    :param slug: 文章的标题别名
    :return: 渲染模板或提交表单后重定向回原页面
    """
    post = Post.objects.get_or_404(slug=slug)

    from_post_author = False
    comment_status = 'pending'
    if current_user.is_authenticated:
        form = UserCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['ORIGINBLOG_ADMIN_EMAIL']
        form.homepage.data = url_for('blog.index')
        if current_user.username == post.author.username:
            from_post_author = True
            comment_status = 'approved'
    else:
        form = CommentForm()

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        homepage = form.homepage.data
        content = form.content.data
        comment = Comment(author=author, email=email, homepage=homepage, content=content, status=comment_status,
                          from_post_author=from_post_author, post_slug=post.slug, post_title=post.title)
        reply_to = request.args.get('replyto')
        if reply_to:
            comment.reply_to = Comment.objects.get_or_404(id=reply_to)

        comment.save()
        flash('Thanks, your comment will be published after reviewed.', 'info')
        return redirect(url_for('blog.show_post', slug=slug))

    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINBLOG_POST_PER_PAGE']
    comment_pagination = Comment.objects.filter(post_slug=post.slug, status='approved').paginate(page,
                                                                                                 per_page=per_page)

    return render_template('blog/post.html', post=post, comment_pagination=comment_pagination, form=form)


@blog_bp.route('/reply/comment/<string:comment_id>')  # TODO:id类型的验证，直接从回复按钮跳转
def reply_comment(comment_id):
    """实现评论的回复功能

    以该视图作为中转传递被回复的评论的id。
    在show_post视图中获取查询参数并进行相应处理。
    :param comment_id: 被回复的comment id
    :return: 跳转到表单填写页面或返回
    """
    comment = Comment.objects.get_or_404(id=comment_id)
    post = Post.objects.get_or_404(slug=comment.post_slug)
    if post.can_comment:
        return redirect(
            url_for('blog.show_post', slug=post.slug, replyto=comment_id,
                    author=comment.author) + '#comment-form')
    else:
        flash('This post is comment disabled.', 'warning')
        return redirect_back()


@blog_bp.route('/author-detail/<string:username>')
def author_detail(username):
    """"""
    author = User.objects.get_or_404(username=username)
    posts = Post.objects.filter(author=author, is_draft=False).order_by('-pub_time')

    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINBLOG_POST_PER_PAGE']
    pagination = posts.paginate(page, per_page=per_page)
    return render_template('blog/author.html', user=author, pagination=pagination)


@blog_bp.route('/achive')
def archive():
    posts = Post.objects.filter(is_draft=False).order_by('-pub_time')

    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINBLOG_POST_PER_PAGE']
    pagination = posts.paginate(page, per_page=per_page)
    return render_template('blog/archive.html', pagination=pagination)


@blog_bp.route('/sitemap.xml/')
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages = []

    posts = Post.objects.filter(is_draft=False)
    for post in posts:
        pages.append((url_for('blog.show_post', slug=post.slug, _external=True),
                      post.update_time.datetime().data().isoformat(), 'weekly', '0.8'))

    sitemap_xml = render_template('blog/sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.header['Content-Type'] = 'application/xml'

    return response
