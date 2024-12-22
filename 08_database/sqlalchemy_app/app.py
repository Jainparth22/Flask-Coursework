"""
Module 08 — Database (Flask-SQLAlchemy)
=========================================
Using Flask-SQLAlchemy ORM for database operations:
models, relationships, CRUD, and querying.

Run:  pip install flask-sqlalchemy
      python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True  # Uncomment to see SQL queries

# Initialize SQLAlchemy with the app
db.init_app(app)


# Create tables on first run
with app.app_context():
    db.create_all()


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    """List all users with their post counts."""
    # Query all users ordered by creation date
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('index.html', users=users)


@app.route('/user/add', methods=['POST'])
def add_user():
    """Create a new user."""
    name = request.form.get('name')
    email = request.form.get('email')
    
    if name and email:
        user = User(name=name, email=email)
        db.session.add(user)
        try:
            db.session.commit()
            flash(f'User {name} created!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'error')
    else:
        flash('Name and email required.', 'error')
    
    return redirect(url_for('index'))


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """Show user details and their posts."""
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    return render_template('user_detail.html', user=user)


@app.route('/user/<int:user_id>/post', methods=['POST'])
def add_post(user_id):
    """Add a post for a user."""
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    
    title = request.form.get('title')
    body = request.form.get('body', '')
    
    if title:
        post = Post(title=title, body=body, author=user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
    
    return redirect(url_for('user_detail', user_id=user_id))


@app.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user and cascade-delete their posts."""
    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.name} deleted.', 'success')
    return redirect(url_for('index'))


# ============================================================
# QUERY EXAMPLES (accessible at /query-examples)
# ============================================================

@app.route('/query-examples')
def query_examples():
    """Demonstrate various SQLAlchemy query methods."""
    examples = {}
    
    # --- SELECT ALL ---
    examples['all_users'] = [u.to_dict() for u in User.query.all()]
    
    # --- FILTER ---
    examples['filter_by_name'] = [u.to_dict() for u in User.query.filter_by(name='Alice').all()]
    
    # --- FILTER with expressions ---
    examples['filter_email_like'] = [u.to_dict() for u in 
        User.query.filter(User.email.like('%example%')).all()]
    
    # --- ORDER BY ---
    examples['ordered_by_name'] = [u.to_dict() for u in 
        User.query.order_by(User.name.asc()).all()]
    
    # --- LIMIT ---
    examples['first_2'] = [u.to_dict() for u in User.query.limit(2).all()]
    
    # --- COUNT ---
    examples['total_count'] = User.query.count()
    
    # --- FIRST (or None) ---
    first = User.query.first()
    examples['first_user'] = first.to_dict() if first else None
    
    # --- GET by primary key ---
    examples['get_by_id_1'] = (lambda u: u.to_dict() if u else None)(db.session.get(User, 1))
    
    # --- PAGINATION ---
    page = User.query.paginate(page=1, per_page=2, error_out=False)
    examples['pagination'] = {
        'items': [u.to_dict() for u in page.items],
        'total': page.total,
        'pages': page.pages,
        'page': page.page,
        'has_next': page.has_next,
        'has_prev': page.has_prev,
    }
    
    from flask import jsonify
    return jsonify(examples)


if __name__ == '__main__':
    # Seed some data if empty
    with app.app_context():
        if User.query.count() == 0:
            alice = User(name='Alice', email='alice@example.com')
            bob = User(name='Bob', email='bob@example.com')
            db.session.add_all([alice, bob])
            db.session.commit()
            
            db.session.add(Post(title='Hello World', body='My first post!', author=alice))
            db.session.add(Post(title='Flask is awesome', body='Loving this framework.', author=alice))
            db.session.add(Post(title='SQLAlchemy tips', body='ORM magic!', author=bob))
            db.session.commit()
    
    app.run(debug=True)
