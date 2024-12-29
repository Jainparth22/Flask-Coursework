"""
Module 11 — Authentication & Authorization
=============================================
Flask-Login for user authentication, password hashing,
login_required decorator, role-based access, and user loader.

Run:  pip install flask-login flask-sqlalchemy flask-wtf
      python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================================================
# FLASK-LOGIN SETUP
# ============================================================

login_manager = LoginManager(app)
login_manager.login_view = 'login'              # Redirect to 'login' if not authenticated
login_manager.login_message = 'Please log in.'   # Flash message
login_manager.login_message_category = 'info'    # Flash category


# ============================================================
# USER MODEL
# ============================================================

class User(UserMixin, db.Model):
    """User model — inherits from UserMixin for Flask-Login integration.
    
    UserMixin provides:
        is_authenticated → True (logged in)
        is_active → True
        is_anonymous → False
        get_id() → returns str(self.id)
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify a password against the hash."""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login callback — load user from session's user_id.
    
    Called on EVERY request if user is logged in.
    Must return a User object or None.
    """
    return db.session.get(User, int(user_id))


# ============================================================
# CUSTOM DECORATORS
# ============================================================

def admin_required(f):
    """Custom decorator — requires admin role."""
    @wraps(f)
    @login_required  # Must be logged in first
    def decorated(*args, **kwargs):
        if not current_user.is_admin():
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # login_user sets the session, optional remember=True for persistent cookie
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to the page user was trying to access (if any)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    """Protected route — only logged-in users."""
    return render_template('profile.html')


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin-only route."""
    users = User.query.all()
    return render_template('admin.html', users=users)


# ============================================================
# INIT
# ============================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create admin user if none exists
        if not User.query.filter_by(role='admin').first():
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
