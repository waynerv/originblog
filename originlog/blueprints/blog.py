from flask import Blueprint, render_template, request, current_app

from originlog.models import Post, Category, Comment

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', default=1, type=int)  # 从查询字符串获取当前页数
    per_page = current_app.config['ORIGINLOG_POST_PER_PAGE']  # 每页数量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)  # 分页对象
    posts = pagination.items  # 当前页数的记录列表
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'Post'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['ORIGINLOG_POST_PER_PAGE']
    pagination = Comment.query.filter(Comment.post_id == post_id).filter(Comment.reviewed == True).order_by(
        Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments)


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
