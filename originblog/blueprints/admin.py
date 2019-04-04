import time
import random
from flask import Blueprint, request, current_app, render_template, flash, redirect, url_for, abort
from flask.views import MethodView
from flask_login import login_required, current_user
from mongoengine import NotUniqueError, DoesNotExist, MultipleObjectsReturned
from mongoengine.queryset import Q

from originblog.forms import PostForm, AboutForm, WidgetForm
from originblog.models import Post, Comment, PostStatistic, Widget, Tracker
from originblog.utils import redirect_back
from originblog.decorator import admin_required, permission_required
from originblog.signals import post_published

admin_bp = Blueprint('admin', __name__)


class AdminIndex(MethodView):
    decorators = [login_required, permission_required('POST')]

    def get(self):
        return render_template('admin/index.html')


class Posts(MethodView):
    """所有文章资源"""
    decorators = [login_required, permission_required('POST')]

    def get(self):  # TODO：对文章内容进行搜索
        """获取所有文章"""
        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['ORIGINBLOG_MANAGE_POST_PER_PAGE']
        post_query = Post.objects.order_by('-update_time', '-weight')

        # 没有审阅权限的用户只能获取自己发表的文章
        if not current_user.can('MODERATE'):
            post_query = post_query.filter(author=current_user._get_current_object())

        pagination = post_query.paginate(page, per_page)
        return render_template('admin/manage_post.html', pagination=pagination)

    def post(self):
        """增加新文章"""
        form = PostForm()

        if form.validate_on_submit():
            title = form.title.data
            abstract = form.abstract.data
            weight = form.weight.data
            raw_content = form.raw_content.data
            category = form.category.data
            tags = form.tag.data.split() if form.tags.data else None
            post = Post(
                title=title,
                abstract=abstract,
                weight=weight,
                raw_content=raw_content,
                category=category,
                tags=tags
            )
            post.author = current_user._get_current_object()
            # 保存文章到数据库时，注意处理slug相同的情况
            try:
                post.save()
            except NotUniqueError:
                post.slug += str(int(time.time()))
                post.save()

            # 初始化文章的统计数据
            post_statistic = PostStatistic(post=post)
            post_statistic.verbose_count_base = random.randint(500, 5000)
            post_statistic.save()

            # 发送文章发布的信号
            post_published.send(current_app._get_current_object(), post=post)

            flash('Post published.', 'success')
            return redirect(url_for('blog.show_post', slug=post.slug))
        return render_template('admin/new_post.html', form=form)


class PostItem(MethodView):
    """单篇文章资源"""
    decorators = [login_required, permission_required('POST')]

    # TODO:管理员发表的文章或评论只有管理员可修改

    def get(self, slug, form=None):
        """获取文章内容与编辑表单"""
        post = Post.objects.get_or_404(slug=slug)
        # 只有管理员或文章作者才有权限修改文章
        if not current_user.is_admin() and post.author != current_user._get_current_object():
            abort(403)

        if not form:
            form = PostForm()
            form.title.data = post.title
            form.abstract.data = post.abstract
            form.weight.data = post.weight
            form.raw_content.data = post.raw_content
            form.category.data = post.category
            form.tag.data = ' '.join(post.tags)

        return render_template('admin/edit_post.html', form=form)

    def put(self, slug):
        """修改文章内容"""
        post = Post.objects.get_or_404(slug)
        # 只有管理员或文章作者才有权限修改文章
        if not current_user.is_admin() and post.author != current_user._get_current_object():
            abort(403)

        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.abstract = form.abstract.data
            post.weight = form.weight.data
            post.raw_content = form.raw_content.data
            post.category = form.category.data
            post.tags = form.tag.data.split() if form.tags.data else None
            # 修改文章包括标题不会更改slug，以确保链接的永久
            post.save()

            flash('Post updated.', 'success')
            return redirect(url_for('blog.show_post', slug=post.slug))
        return self.get(slug, form)

    def patch(self, slug):
        """设置文章是否可评论"""
        post = Post.objects.get_or_404(slug)
        # 拥有审阅权限才能设置文章是否可评论
        if not current_user.can('MODERATE'):
            abort(403)

        if post.can_comment:
            post.can_comment = False
            flash('Comment disabled.', 'success')
        else:
            post.can_comment = True
            flash('Comment enabled.', 'success')
        post.save()

        return redirect_back()  # TODO：该操作需要附加next参数

    def delete(self, slug):
        """删除文章"""
        post = Post.objects.get_or_404(slug)
        # 需要有审核权限或文章作者才能够删除文章
        if not current_user.can('MODERATE') and post.author != current_user._get_current_object():
            abort(403)

        try:
            post_statistic = PostStatistic.objects.get(post=post)
            post_statistic.delete()
        except (MultipleObjectsReturned, DoesNotExist):
            pass

        post.delete()
        flash('Post deleted.', 'success')
        return redirect_back()  # TODO：删除操作需要附加next参数


class Comments(MethodView):
    """所有评论资源"""
    decorator = [login_required, permission_required('MODERATE')]

    def get(self):
        """获取评论列表,可进行分类筛选"""
        filter_rule = request.args.get('filter', 'all')  # TODO：对评论字符串内容进行搜索
        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['ORIGINBLOG_MANAGE_COMMENT_PER_PAGE']

        if filter_rule == 'all':
            filter_comments = Comment.objects
        elif filter_rule == 'pending':
            filter_comments = Comment.objects.filter(status='pending')
        elif filter_rule == 'admin':
            filter_comments = Comment.objects.filter(from_admin=True)

        pagination = filter_comments.order_by('-pub_time').paginate(page, per_page)
        comments = pagination.items  # TODO:统一传入模板格式
        return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)

    def delete(self):
        """删除所有未审核的及标记为垃圾信息的评论"""
        comments = Comment.objects(Q(status='pending') | Q(status='spam'))
        comments.delete()
        flash('All pending comments and spams has been deleted', 'success')
        return redirect_back()  # TODO：删除操作需要附加next参数


class CommentItem(MethodView):
    """单条评论资源（不可修改内容）"""
    decorators = [login_required, permission_required('MODERATE')]

    def patch(self, pk):  # pk为Comment模型的主键，默认为Comment.id(即_id)
        """更改评论审核状态"""
        comment = Comment.objects.get_or_404(pk=pk)
        if request.form['status'] == 'approved':
            comment.status = 'approved'
        elif request.form['status'] == 'spam':
            comment.status = 'approved'
        comment.save()

        flash('Comment approved.', 'success')
        return redirect_back()  # TODO：审核操作需要附加next参数

    def delete(self, pk):
        """删除评论"""
        comment = Comment.objects.get_or_404(pk=pk)
        if not current_user.is_admin() and comment.from_admin:
            abort(403)

        comment.delete()
        flash('Comment deleted.', 'success')
        return redirect_back()  # TODO：审核操作需要附加next参数


class Widgets(MethodView):
    """所有widget资源"""
    decorators = [login_required, admin_required]

    def get(self):
        """获取widget列表"""
        widgets = Widget.objects.all()

        return render_template('admin/manage_widget.html', widgets=widgets)

    def post(self):
        """新增widget"""
        form = WidgetForm()

        if form.validate_on_submit():
            title = form.title.data
            priority = form.priority.data
            widget = Widget(title=title, priority=priority)
            if form.content_type.data == 'html':
                widget.html_content = form.content.data
                widget.raw_content = None
            else:
                widget.raw_content = form.content.data
            widget.save()

            flash('Widget created.', 'success')
            return redirect(url_for('admin.manage_link'))
        return render_template('admin/new_widget.html', form=form)


class WidgetItem(MethodView):
    """单个widget资源"""
    decorators = [login_required, admin_required]

    def get(self, pk, form=None):
        """获取widget内容与编辑表单"""
        widget = Widget.objects.get_or_404(pk)

        if not form:
            form = WidgetForm()
            form.title = widget.title
            form.priority = widget.priority
            if widget.raw_content:
                form.content_type = 'markdown'
                form.content = widget.raw_content
            else:
                form.content_type = 'html'
                form.content = widget.html_content
        return render_template('admin/edit_widget.html', form=form)

    def put(self, pk):
        """修改widget内容"""
        widget = Widget.objects.get_or_404(pk)

        form = WidgetForm
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
            return redirect(url_for('admin/manage_widget'))
        return self.get(pk, form)

    def delete(self, pk):
        """删除widget"""
        widget = Widget.objects.get_or_404(pk)
        widget.delete()
        flash('Widget deleted.', 'success')
        return redirect_back()  # TODO：审核操作需要附加next参数


class PostStatistics(MethodView):
    """所有文章统计信息资源"""
    decorators = [login_required, admin_required]

    def get(self):
        """获取文章统计信息列表"""
        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['ORIGINBLOG_MANAGE_POST_PER_PAGE']
        pagination = PostStatistic.objects.paginate(page, per_page)
        return render_template('admin/manage_statistic.html', pagination=pagination)


class PostStatisticItem(MethodView):
    """单篇文章统计信息资源"""
    decorators = [login_required, admin_required]

    def get(self, slug):
        """获取指定文章的统计信息和浏览记录"""
        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config['ORIGINBLOG_MANAGE_POST_PER_PAGE']

        post = Post.objects.get_or_404(slug=slug)
        post_statistic = PostStatistics.objects.get_or_404(post=post)
        tracker_pagination = Tracker.objects.filter(post=post).paginate(page, per_page)
        return render_template('admin/show_statistic', post_statistic=post_statistic, trackers=tracker_pagination)


# 注册路由
admin_bp.add_url_rule('/', view_func=Posts.as_view('index'), methods=['GET'])

admin_bp.add_url_rule('/posts', view_func=Posts.as_view('posts'), methods=['GET', 'POST'])
admin_bp.add_url_rule('/posts/<slug>', view_func=Posts.as_view('post'), methods=['GET', 'PUT', 'PATCH', 'DELETE'])

admin_bp.add_url_rule('/posts/comments', view_func=Comments.as_view('comments'), methods=['GET', 'POST'])
admin_bp.add_url_rule('/posts/comments/<pk>', view_func=CommentItem.as_view('comment'), methods=['PATCH', 'DELETE'])

admin_bp.add_url_rule('/widgets', view_func=Widgets.as_view('widgets'), methods=['GET', 'POST'])
admin_bp.add_url_rule('/widgets/<pk>', view_func=WidgetItem.as_view('widget'), methods=['GET', 'PUT', 'DELETE'])

admin_bp.add_url_rule('/posts/statistics', view_func=PostStatistics.as_view('statistics'), methods=['GET'])
admin_bp.add_url_rule('/posts/statistics/<slug>', view_func=PostStatisticItem.as_view('statistic'), methods=['GET'])


# @admin_bp.route('/settings', methods=['GET', 'POST'])
# @login_required
# def settings():
#     form = AboutForm()
#     admin = Admin.query.first_or_404()
#
#     if form.validate_on_submit():
#         admin.blog_title = form.blog_title.data
#         admin.blog_sub_title = form.blog_sub_title.data
#         admin.about = form.about.data
#         db.session.commit()
#         flash('Settings updated.', 'success')
#         return redirect(url_for('blog.index'))
#
#     form.blog_title.data = admin.blog_title
#     form.blog_sub_title.data = admin.blog_sub_title
#     form.about.data = admin.about
#     return render_template('admin/edit_about.html', form=form)
