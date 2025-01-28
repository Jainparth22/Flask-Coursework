"""Main Blueprint — public pages."""

from flask import Blueprint, render_template
from blog.models import Post

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)
