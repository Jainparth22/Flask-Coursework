# Module 11 — Authentication & Authorization | Documentation

## Overview

Flask-Login handles user session management. Werkzeug provides password hashing. Together they form a complete auth system.

> 📖 **Flask-Login Docs**: [Flask-Login](https://flask-login.readthedocs.io/)  
> 📖 **Official Docs**: [Security — Hashing](https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.security.generate_password_hash)

---

## 1. Flask-Login Setup

```python
from flask_login import LoginManager

login_manager = LoginManager(app)
login_manager.login_view = 'login'          # Redirect for @login_required
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

## 2. User Model (UserMixin)

```python
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # UserMixin provides: is_authenticated, is_active, is_anonymous, get_id()
```

## 3. Password Hashing

```python
from werkzeug.security import generate_password_hash, check_password_hash

hash = generate_password_hash('password')    # → 'scrypt:...'
check_password_hash(hash, 'password')        # → True
check_password_hash(hash, 'wrong')           # → False
```

## 4. Login / Logout

```python
from flask_login import login_user, logout_user, current_user

login_user(user, remember=True)    # Set session
logout_user()                       # Clear session
current_user.username              # Access logged-in user anywhere
current_user.is_authenticated       # True if logged in
```

## 5. Protecting Routes

```python
@app.route('/profile')
@login_required            # Redirects to login_view if not authenticated
def profile():
    return f'Hello {current_user.username}'
```

## 6. Custom Authorization Decorator

```python
from functools import wraps

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated
```

## 7. `next` Parameter (Redirect After Login)

```python
next_page = request.args.get('next')
return redirect(next_page or url_for('index'))
```

When `@login_required` redirects to login, it adds `?next=/profile` so after login the user goes back to the original page.

---

## Key Takeaways
- `UserMixin` provides required properties for Flask-Login
- **Never** store plain passwords — always hash with `generate_password_hash()`
- `@login_required` protects routes; `current_user` is a global proxy
- Custom decorators for role-based access (admin, moderator, etc.)
