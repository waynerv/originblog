from flask import Blueprint, render_template, request, current_app

from originlog.models import Post

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', default=1, type=int)  # 从查询字符串获取当前页数
    per_page = current_app.config['ORIGINLOG_POST_PER_PAGE']  # 每页数量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)  # 分页对象
    posts = pagination.items  # 当前页数的记录列表
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'Post'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post.html', post=post)


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/categoroy.html')


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')
