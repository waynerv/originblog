import random
import time

from flask import request, current_app, render_template, flash, redirect, url_for, abort, jsonify
from flask.views import MethodView
from flask_login import current_user
from mongoengine import NotUniqueError, DoesNotExist, MultipleObjectsReturned
from mongoengine.queryset import Q

from originblog.decorator import admin_required, permission_required
from originblog.forms.admin import PostForm, WidgetForm, MetaPostForm, MetaUserForm
from originblog.forms.auth import RegisterForm
from originblog.models import Post, Comment, PostStatistic, Widget, Tracker, User, Role
from originblog.signals import post_published
from originblog.emails import send_new_comment_email, send_new_reply_email


class AdminIndex(MethodView):
    decorators = [permission_required('POST')]

    def get(self):
        post_count = Post.objects.count()
        comment_count = Comment.objects.count()
        user_count = User.objects.count()
        read_count = PostStatistic.objects.aggregate(
            {'$group': {
                '_id': 'null',
                'count': {'$sum': '$visit_count'}
            }}
        )
        # 将聚合操作返回的可迭代游标对象转换成列表
        read_count = list(read_count)
        recent_posts = Post.objects.filter(type='post').limit(10)
        recent_comments = Comment.objects.limit(10)
        return render_template('admin/admin_index.html', posts=post_count, comments=comment_count, users=user_count,
                               reads=read_count, recent_posts=recent_posts, recent_comments=recent_comments)


class Posts(MethodView):
    """所有文章资源"""
    decorators = [permission_required('POST')]

    def get(self, post_type='post'):
        """获取所有文章"""
        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['APP_MANAGE_POST_PER_PAGE']
        post_query = Post.objects.filter(type=post_type).order_by('-update_time', '-weight')

        # 没有审阅权限的用户只能获取自己发表的文章
        if not current_user.can('MODERATE'):
            post_query = post_query.filter(author=current_user._get_current_object())

        pagination = post_query.paginate(page, per_page)
        templates = {
            'post': 'admin/manage_post.html',
            'page': 'admin/manage_page.html'
        }
        return render_template(templates.get(post_type, 'admin/manage_post.html'), pagination=pagination)

    def post(self):
        """增加新文章"""
        form = PostForm()

        if form.validate_on_submit():
            title = form.title.data
            abstract = form.abstract.data
            weight = form.weight.data
            raw_content = form.raw_content.data
            category = form.category.data if form.category.data else None
            tags = form.tags.data.split() if form.tags.data else None
            type = form.type.data
            post = Post(
                title=title,
                abstract=abstract,
                weight=weight,
                raw_content=raw_content,
                category=category,
                tags=tags,
                type=type
            )
            post.author = current_user._get_current_object()
            if post.author.is_admin:
                post.from_admin = True
            # 保存文章到数据库时，注意处理slug相同的情况
            try:
                post.save()
            except NotUniqueError:
                post.slug += str(int(time.time()))
                post.save()

            # 初始化文章的统计数据
            post_statistic = PostStatistic(post=post, post_type=post.type)
            post_statistic.verbose_count_base = random.randint(500, 5000)
            post_statistic.save()

            # 发送文章发布的信号
            post_published.send(current_app._get_current_object(), post=post)

            flash('Post published.', 'success')
            # 跳转到对应端点
            endpoints = {
                'post': 'blog.show_post',
                'page': 'blog.show_page'
            }
            return redirect(url_for(endpoints[post.type], slug=post.slug))
        templates = {
            'post': 'admin/new_post.html',
            'page': 'admin/new_page.html'
        }
        return render_template(templates.get(form.type.data, 'admin/new_post.html'), form=form)


class PostItem(MethodView):
    """单篇文章资源"""
    decorators = [permission_required('POST')]

    def get(self, slug, form=None):
        """获取文章内容与编辑表单"""
        post = Post.objects.get_or_404(slug=slug)
        # 只有管理员或文章作者才有权限修改文章内容
        if not current_user.is_admin and post.author != current_user._get_current_object():
            abort(403)

        if not form:
            form = PostForm()
            form.title.data = post.title
            form.abstract.data = post.abstract
            form.weight.data = post.weight
            form.raw_content.data = post.raw_content
            form.category.data = post.category
            form.tags.data = ' '.join(post.tags)
            form.type.data = post.type

        templates = {
            'post': 'admin/edit_post.html',
            'page': 'admin/edit_page.html'
        }
        return render_template(templates.get(post.type, 'admin/edit_post.html'), slug=slug, form=form)

    def post(self, slug):
        """修改文章内容"""
        post = Post.objects.get_or_404(slug=slug)
        # 只有管理员或文章作者才有权限修改文章
        if not current_user.is_admin and post.author != current_user._get_current_object():
            abort(403)

        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.abstract = form.abstract.data
            post.weight = form.weight.data
            post.raw_content = form.raw_content.data
            post.category = form.category.data if form.category.data else None
            post.tags = form.tags.data.split() if form.tags.data else None
            post.type = form.type.data
            # 修改文章包括标题不会更改slug，以确保链接的永久
            post.save()

            flash('Post updated.', 'success')
            post_type = post.type
            endpoints = {
                'post': 'blog.show_post',
                'page': 'blog.show_page'
            }
            return redirect(url_for(endpoints[post_type], slug=post.slug))
        return self.get(slug, form)

    def patch(self, slug):
        """设置文章是否可评论"""
        post = Post.objects.get_or_404(slug=slug)
        # 拥有审核权限才能设置文章是否可评论,管理员的文章只有管理员可设置
        if not current_user.can('MODERATE'):
            jsonify(message='No Permission.'), 403
        elif not current_user.is_admin and post.from_admin:
            jsonify(message='No Permission.'), 403

        if post.can_comment:
            post.can_comment = False
            message = 'Comment disabled.'
        else:
            post.can_comment = True
            message = 'Comment enabled.'
        post.save()
        return jsonify(message=message)

    def delete(self, slug):
        """删除文章"""
        post = Post.objects.get_or_404(slug=slug)

        # 需要有审核权限或文章作者才能够删除文章，管理员的文章只有管理员可删除
        if not current_user.can('MODERATE') and post.author != current_user._get_current_object():
            return jsonify(message='No Permission.'), 403
        elif not current_user.is_admin and post.from_admin:
            return jsonify(message='No Permission.'), 403

        try:
            post_statistic = PostStatistic.objects.get(post=post)
            post_statistic.delete()
        except (MultipleObjectsReturned, DoesNotExist):
            pass

        post.delete()

        # 如果是删除后重载页面的请求，通过flash发送通知
        data = request.get_json()
        if data and data.get('flash'):
            flash('Post deleted.', 'success')
        return jsonify(message='Post deleted.')


class MetaPosts(MethodView):
    """所有文章元资源"""
    decorators = [admin_required]

    def get(self):
        """获取所有文章"""
        filter_rule = request.args.get('filter', 'all')
        if filter_rule == 'all':
            filter_posts = Post.objects
        elif filter_rule == 'post':
            filter_posts = Post.objects.filter(type='post')
        elif filter_rule == 'page':
            filter_posts = Post.objects.filter(type='page')
        else:
            filter_posts = Post.objects

        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['APP_MANAGE_POST_PER_PAGE']
        pagination = filter_posts.order_by('-update_time', '-weight').paginate(page, per_page)
        return render_template('admin/manage_article.html', pagination=pagination)

    def post(self):
        """增加新文章"""
        form = MetaPostForm()

        if form.validate_on_submit():
            title = form.title.data
            slug = form.slug.data
            abstract = form.abstract.data
            raw_content = form.raw_content.data
            pub_time = form.pub_time.data
            category = form.category.data if form.category.data else None
            tags = form.tags.data.split() if form.tags.data else None
            weight = form.weight.data
            can_comment = form.can_comment.data
            type = form.type.data
            post = Post(
                title=title,
                slug=slug,
                abstract=abstract,
                pub_time=pub_time,
                raw_content=raw_content,
                category=category,
                tags=tags,
                weight=weight,
                can_comment=can_comment,
                type=type
            )
            post.author = current_user._get_current_object()
            # 保存文章到数据库时，注意处理slug相同的情况
            try:
                post.save()
            except NotUniqueError:
                post.slug += str(int(time.time()))
                post.save()

            # 初始化文章的统计数据
            post_statistic = PostStatistic(post=post, post_type=post.type)
            post_statistic.verbose_count_base = random.randint(500, 5000)
            post_statistic.save()

            # 发送文章发布的信号
            post_published.send(current_app._get_current_object(), post=post)

            flash('Post published.', 'success')
            # 跳转到对应端点
            endpoints = {
                'post': 'blog.show_post',
                'page': 'blog.show_page'
            }
            return redirect(url_for(endpoints[post.type], slug=post.slug))
        return render_template('admin/new_article.html', form=form)


class MetaPostItem(MethodView):
    """单篇文章元资源"""
    decorators = [admin_required]

    def get(self, slug, form=None):
        """获取文章内容与编辑表单"""
        post = Post.objects.get_or_404(slug=slug)

        if not form:
            form = MetaPostForm()
            form.title.data = post.title
            form.abstract.data = post.abstract
            form.weight.data = post.weight
            form.raw_content.data = post.raw_content
            form.pub_time.data = post.pub_time
            form.category.data = post.category
            form.tags.data = ' '.join(post.tags)
            form.can_comment.data = post.can_comment
            form.type.data = post.type

        return render_template('admin/edit_article.html', slug=slug, form=form)

    def post(self, slug):
        """修改文章内容"""
        form = MetaPostForm()
        if form.validate_on_submit():
            post = Post.objects.get_or_404(slug=slug)
            post.title = form.title.data
            post.abstract = form.abstract.data
            post.raw_content = form.raw_content.data
            post.pub_time = form.pub_time.data
            post.category = form.category.data if form.category.data else None
            post.tags = form.tags.data.split() if form.tags.data else None
            post.weight = form.weight.data
            post.can_comment = form.can_comment.data
            post.type = form.type.data
            # 修改文章包括标题不会更改slug，以确保链接的永久
            post.save()

            flash('Post updated.', 'success')
            endpoints = {
                'post': 'blog.show_post',
                'page': 'blog.show_page'
            }
            return redirect(url_for(endpoints[post.type], slug=post.slug))
        return self.get(slug, form)


class Comments(MethodView):
    """所有评论资源"""
    decorator = [permission_required('MODERATE')]

    def get(self):
        """获取评论列表,可进行分类筛选"""
        filter_rule = request.args.get('filter', 'all')
        if filter_rule == 'all':
            filter_comments = Comment.objects
        elif filter_rule == 'unread':
            filter_comments = Comment.objects.filter(status='pending')
        elif filter_rule == 'admin':
            filter_comments = Comment.objects.filter(from_admin=True)
        else:
            filter_comments = Comment.objects

        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['APP_MANAGE_COMMENT_PER_PAGE']
        pagination = filter_comments.order_by('-pub_time').paginate(page, per_page)
        return render_template('admin/manage_comment.html', pagination=pagination)

    def delete(self):
        """删除所有未审核的及标记为垃圾信息的评论"""
        comments = Comment.objects(Q(status='pending') | Q(status='spam'))
        comments.delete()
        flash('All pending comments and spams has been deleted', 'success')
        return jsonify(message='All pending comments and spams has been deleted')


class CommentItem(MethodView):
    """单条评论资源（不可修改内容）"""
    decorators = [permission_required('MODERATE')]

    def patch(self, pk):  # pk为Comment模型的主键，默认为Comment.id(即_id)
        """更改评论审核状态"""
        comment = Comment.objects.get_or_404(pk=pk)
        post = Post.objects.get_or_404(slug=comment.post_slug)
        data = request.get_json()
        if data['operation'] == 'approve':
            comment.status = 'approved'
            message = 'Comment approved.'
            send_new_comment_email(post)
            if comment.reply_to:
                send_new_reply_email(comment.reply_to)
        elif data['operation'] == 'spam':
            comment.status = 'spam'
            message = 'Spam marked.'
        else:
            message = 'Invalid operation'
        comment.save()

        # flash('Comment approved.', 'success')
        return jsonify(message=message)

    def delete(self, pk):
        """删除评论"""
        comment = Comment.objects.get_or_404(pk=pk)
        # 来自管理员的评论只有管理员自己可以删除
        if not current_user.is_admin and comment.from_admin:
            return jsonify(message='No Permission.'), 403

        comment.delete()
        # flash('Comment deleted.', 'success')
        return jsonify(message='Comment deleted.')


class Users(MethodView):
    """所有用户"""
    decorator = [permission_required('MODERATE')]

    def get(self):
        """获取所有用户列表"""
        filter_rule = request.args.get('filter', 'all')
        if filter_rule == 'all':
            filter_users = User.objects
        elif filter_rule == 'writer':
            role = Role.objects.filter(role_name='writer').first()
            filter_users = User.objects.filter(role=role)
        elif filter_rule == 'moderator':
            role = Role.objects.filter(role_name='moderator').first()
            filter_users = User.objects.filter(role=role)
        elif filter_rule == 'admin':
            role = Role.objects.filter(role_name='admin').first()
            filter_users = User.objects.filter(role=role)
        else:
            filter_users = User.objects

        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['APP_MANAGE_USER_PER_PAGE']
        pagination = filter_users.paginate(page, per_page)
        return render_template('admin/manage_user.html', pagination=pagination)

    def post(self):
        """手动添加新用户"""
        form = RegisterForm()

        if form.validate_on_submit():
            name = form.name.data
            username = form.username.data
            email = form.email.data.lower()
            password = form.password.data
            user = User(
                name=name,
                username=username,
                email=email
            )
            user.set_password(password)
            user.email_confirmed = True
            user.save()
            flash('User created.', 'success')
            return self.get()
        return render_template('admin/new_user.html', form=form)


class MetaUserItem(MethodView):
    decorators = [admin_required]

    def get(self, pk, form=None):
        """获取用户资料与表单"""
        user = User.objects.get_or_404(pk=pk)

        if not form:
            form = MetaUserForm(user)
            form.username.data = user.username
            form.email.data = user.email
            form.email_confirmed.data = user.email_confirmed
            form.name.data = user.name
            form.bio.data = user.bio
            form.homepage.data = user.homepage
            form.weibo.data = user.social_networks['weibo'].get('url')
            form.weixin.data = user.social_networks['weixin'].get('url')
            form.github.data = user.social_networks['github'].get('url')
            form.role.data = user.role.role_name
            form.active.data = user.active

        return render_template('admin/edit_user.html', pk=pk, form=form)

    def post(self, pk):
        """修改用户资料"""
        user = User.objects.get_or_404(pk=pk)
        form = MetaUserForm(user)
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.email_confirmed = form.email_confirmed.data
            user.name = form.name.data
            user.bio = form.bio.data
            user.homepage = form.homepage.data
            user.social_networks['weibo']['url'] = form.weibo.data
            user.social_networks['weixin']['url'] = form.weixin.data
            user.social_networks['github']['url'] = form.github.data
            user.role = Role.objects.filter(role_name=form.role.data).first() or Role.objects.filter(
                role_name='reader').first()
            user.active = form.active.data
            user.save()

            flash('User updated', 'success')
            return redirect(url_for('admin.users'))
        return self.get(pk, form)

    def delete(self, pk):
        """删除用户"""
        user = User.objects.get_or_404(pk=pk)
        if user.is_admin:
            return jsonify(message='Admin cannot be deleted.'), 403
        user.delete()
        # flash('User deleted.', 'success')
        return jsonify(message='User deleted.')


class Widgets(MethodView):
    """所有widget资源"""
    decorators = [admin_required]

    def get(self):
        """获取widget列表"""
        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['APP_MANAGE_WIDGET_PER_PAGE']
        pagination = Widget.objects.paginate(page, per_page)
        return render_template('admin/manage_widget.html', pagination=pagination)

    def post(self):
        """新增widget"""
        form = WidgetForm()

        if form.validate_on_submit():
            title = form.title.data
            priority = form.priority.data
            widget = Widget(title=title, priority=priority)
            if form.content_type.data == 'markdown':
                widget.raw_content = form.content.data
            else:
                widget.html_content = form.content.data
                widget.raw_content = None
            widget.save()

            flash('Widget created.', 'success')
            return redirect(url_for('admin.widgets'))
        return render_template('admin/new_widget.html', form=form)


class WidgetItem(MethodView):
    """单个widget资源"""
    decorators = [admin_required]

    def get(self, pk, form=None):
        """获取widget内容与编辑表单"""
        widget = Widget.objects.get_or_404(pk=pk)

        if not form:
            form = WidgetForm()
            form.title.data = widget.title
            form.priority.data = widget.priority
            if widget.raw_content:
                form.content_type.data = 'markdown'
                form.content.data = widget.raw_content
            else:
                form.content_type.data = 'html'
                form.content.data = widget.html_content
        return render_template('admin/edit_widget.html', pk=pk, form=form)

    def post(self, pk):
        """修改widget内容"""
        widget = Widget.objects.get_or_404(pk=pk)

        form = WidgetForm()
        if form.validate_on_submit():
            widget.title = form.title.data
            widget.priority = form.priority.data
            if form.content_type.data == 'html':
                widget.html_content = form.content.data
                widget.raw_content = None  # 清除原有内容
            else:
                widget.raw_content = form.content.data
            widget.save()

            flash('Widget updated.', 'success')
            return redirect(url_for('admin.widgets'))
        return self.get(pk, form)

    def delete(self, pk):
        """删除widget"""
        widget = Widget.objects.get_or_404(pk=pk)
        widget.delete()
        # flash('Widget deleted.', 'success')
        return jsonify(message='Widget deleted.')


class PostStatistics(MethodView):
    """所有文章统计信息资源"""
    decorators = [admin_required]

    def get(self):
        """获取文章统计信息列表"""
        filter_rule = request.args.get('filter', 'all')
        if filter_rule == 'all':
            filter_statistics = PostStatistic.objects.order_by('-pk')
        elif filter_rule == 'post':
            filter_statistics = PostStatistic.objects.filter(post_type='post').order_by('-pk')
        elif filter_rule == 'page':
            filter_statistics = PostStatistic.objects.filter(post_type='page').order_by('-pk')
        else:
            filter_statistics = PostStatistic.objects

        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['APP_MANAGE_STATISTIC_PER_PAGE']
        pagination = filter_statistics.paginate(page, per_page)
        return render_template('admin/manage_statistic.html', pagination=pagination)


class PostStatisticItem(MethodView):
    """单篇文章统计信息资源"""
    decorators = [admin_required]

    def get(self, slug):
        """获取指定文章的统计信息和浏览记录"""
        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['APP_MANAGE_TRACKER_PER_PAGE']

        post = Post.objects.get_or_404(slug=slug)
        post_statistic = PostStatistic.objects.get_or_404(post=post)
        pagination = Tracker.objects.filter(post=post).paginate(page, per_page)
        return render_template('admin/show_statistic.html', post_statistic=post_statistic, pagination=pagination)
