from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, make_response
from flask_login import current_user
from mongoengine.queryset.visitor import Q

from originblog.forms.blog import CommentForm, UserCommentForm
from originblog.models import Post, Comment, Widget
from originblog.signals import post_visited
from originblog.utils import redirect_back, reply_filter

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """构建博客首页

    查询所有已发表的文章，根据分类、标签、关键字搜索等特定查询参数进行筛选分页
    """
    # 获取已发表并且权重值大于0的文章的QuerySet，按权重和发表时间排序
    pub_posts = Post.objects.filter(type='post').order_by('-weight', '-pub_time')
    posts = pub_posts.filter(Q(weight__gt=0) | Q(weight=None))

    # 根据查询参数获取特定分类的文章
    category = request.args.get('category')
    if category:
        posts = posts.filter(category=category)

    # 根据查询参数获取特定标签的文章
    tag = request.args.get('tag')
    if tag:
        posts = posts.filter(tags=tag)

    # 根据查询参数获取特定文本关键词的搜索结果
    keywords = request.args.get('keywords')
    if keywords:
        posts = posts.filter(Q(raw_content__icontains=keywords) | Q(title__icontains=keywords))

    # 获取首页所有widgets
    widgets = Widget.objects

    # 从查询参数获取当前页数并对QuerySet分页
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['APP_POST_PER_PAGE']
    pagination = posts.paginate(page, per_page=per_page)  # 分页对象

    return render_template('blog/index.html', pagination=pagination, widgets=widgets, cur_category=category,
                           cur_tag=tag, cur_keywords=keywords)


@blog_bp.route('/posts/<slug>', methods=['GET', 'POST'])
def show_post(slug, post_type='post'):
    """显示文章正文、评论列表与评论表单并处理表单提交。

    已登录用户不需要手动填写评论表单的个人信息,通过查询参数reply-to判断是否为评论回复，并进行相应处理
    :param slug: 文章的标题别名
    :param post_type: 显示的文章类型（用来区分专用页面）
    """
    post = Post.objects.get_or_404(slug=slug)

    # 若用户为认证用户，使用专门的评论表单
    if current_user.is_authenticated:
        form = UserCommentForm()
        form.author.data = current_user.name
        form.email.data = current_user.email
        form.homepage.data = current_user.homepage
    else:
        form = CommentForm()

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        homepage = form.homepage.data
        md_content = form.content.data
        comment = Comment(author=author, email=email, homepage=homepage, md_content=md_content, post_slug=post.slug,
                          post_title=post.title)
        reply_to = request.args.get('replyto')
        if reply_to:
            comment.reply_to = Comment.objects.get_or_404(pk=reply_to)
        message = 'Thanks, your comment will be published after reviewed.'
        # 管理员和文章作者发布的评论不需要审核
        if current_user.is_authenticated and current_user.username == post.author.username:
            comment.from_post_author = True
            comment.status = 'approved'
            message = 'Comment published.'
        if current_user.is_admin:
            comment.from_admin = True
            comment.status = 'approved'
            message = 'Comment published.'

        comment.save()
        flash(message, 'info')
        # 根据文章类型使用不同的端点
        endpoints = {
            'post': 'blog.show_post',
            'page': 'blog.show_page'
        }
        return redirect(url_for(endpoints[post_type], slug=slug))

    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['APP_COMMENT_PER_PAGE']
    comment_pagination = Comment.objects.filter(post_slug=post.slug, status='approved').paginate(page, per_page)
    # 发送文章被浏览的信号
    post_visited.send(current_app._get_current_object(), post=post)
    # 根据文章类型使用不同的模板
    templates = {
        'post': 'blog/post.html',
        'page': 'blog/page.html'
    }

    return render_template(templates.get(post_type, 'blog/post.html'), post=post, comment_pagination=comment_pagination,
                           form=form, reply_filter=reply_filter)


# 为专用页面page注册路由
blog_bp.add_url_rule('/pages/<slug>/', 'show_page', show_post, defaults={'post_type': 'page'}, methods=['GET', 'POST'])


@blog_bp.route('/reply/comment/<pk>', defaults={'post_type': 'post'})
@blog_bp.route('/reply/<post_type>/comment/<pk>')
def reply_comment(pk, post_type):
    """实现评论的回复功能

    以该视图作为中转传递被回复的评论的id。
    在show_post视图中获取查询参数并进行相应处理。
    :param pk: 被回复的comment id
    :param post_type: 发表评论的文章类型
    """
    comment = Comment.objects.get_or_404(pk=pk)
    post = Post.objects.get_or_404(slug=comment.post_slug)
    if post.can_comment:
        endpoints = {
            'post': 'blog.show_post',
            'page': 'blog.show_page'
        }
        return redirect(
            url_for(endpoints[post_type], slug=post.slug, replyto=pk,
                    author=comment.author) + '#comments')
    else:
        flash('This post is comment disabled.', 'warning')
        return redirect_back()


@blog_bp.route('/archive')
def archive():
    """按时间归档文章"""
    posts = Post.objects.filter(type='post').order_by('-pub_time').only('title', 'slug', 'pub_time')
    # 按月份分组所有post
    data = {}
    years = reversed(list(set([post.pub_time.year for post in posts])))
    for year in years:
        months = reversed(list(set([post.pub_time.month for post in posts if post.pub_time.year == year])))
        for month in months:
            post_items = [post for post in posts if post.pub_time.month == month]
            data[(year, month)] = post_items
    return render_template('blog/archive.html', data=data)


@blog_bp.route('/sitemap.xml/')
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages = []

    posts = Post.objects
    for post in posts:
        post_type = post.type
        endpoints = {
            'post': 'blog.show_post',
            'page': 'blog.show_page'
        }
        pages.append((url_for(endpoints[post_type], slug=post.slug, _external=True),
                      post.update_time.date(), 'weekly', '0.8'))

    sitemap_xml = render_template('blog/sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'

    return response
