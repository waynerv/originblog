from flask import Blueprint, render_template
from originlog.models import Post

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/index.html', posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'Post'])
def show_post(post_id):
    return render_template('blog/post.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/categoroy.html')

