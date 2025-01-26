"""Posts Blueprint — Create, Read, Update, Delete posts."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from blog.extensions import db
from blog.models import Post

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title and body:
            post = Post(title=title, body=body, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post published!', 'success')
            return redirect(url_for('main.index'))
        flash('Title and body required.', 'error')
    return render_template('posts/new.html')


@posts_bp.route('/<int:post_id>')
def view_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('main.index'))
    return render_template('posts/view.html', post=post)


@posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = db.session.get(Post, post_id)
    if not post or post.user_id != current_user.id:
        flash('Not allowed.', 'error')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        post.title = request.form['title']
        post.body = request.form['body']
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    return render_template('posts/edit.html', post=post)


@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if not post or post.user_id != current_user.id:
        flash('Not allowed.', 'error')
        return redirect(url_for('main.index'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(url_for('main.index'))
