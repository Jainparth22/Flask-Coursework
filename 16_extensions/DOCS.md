# Module 16 — Flask Extensions | Documentation

## Overview

The Flask ecosystem has extensions for nearly everything. This module covers the most commonly used ones.

> 📖 **Official Docs**: [Extensions](https://flask.palletsprojects.com/en/stable/extensions/)

---

## 1. Flask-Caching

```bash
pip install Flask-Caching
```

```python
from flask_caching import Cache

app.config['CACHE_TYPE'] = 'SimpleCache'  # or 'RedisCache', 'MemcachedCache'
cache = Cache(app)

@app.route('/data')
@cache.cached(timeout=60)
def data():
    return expensive_query()

# Manual caching
cache.set('key', 'value', timeout=300)
cache.get('key')
cache.delete('key')
cache.clear()

# Memoize (cache by function arguments)
@cache.memoize(timeout=60)
def get_user(user_id):
    return db.session.get(User, user_id)
```

---

## 2. Flask-CORS

```bash
pip install Flask-CORS
```

```python
from flask_cors import CORS

CORS(app)  # Allow all origins
CORS(app, resources={r'/api/*': {'origins': 'http://localhost:3000'}})
```

---

## 3. Flask-Limiter

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address, app=app,
    default_limits=['200/day', '50/hour'])

@app.route('/api')
@limiter.limit('10/minute')
def api(): ...

@app.route('/health')
@limiter.exempt
def health(): ...
```

---

## 4. Flask-Migrate (Alembic)

```bash
pip install Flask-Migrate
```

```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```

```bash
flask db init          # Create migrations folder
flask db migrate -m "Add users table"   # Generate migration
flask db upgrade       # Apply migration
flask db downgrade     # Revert last migration
flask db history       # Show migration history
```

---

## 5. Flask-Mail

```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

msg = Message('Subject', sender='you@gmail.com', recipients=['them@gmail.com'])
msg.body = 'Plain text body'
msg.html = '<h1>HTML body</h1>'
mail.send(msg)
```

---

## Popular Extensions Reference

| Extension | Purpose |
|-----------|---------|
| Flask-SQLAlchemy | ORM |
| Flask-Migrate | Database migrations |
| Flask-Login | User authentication |
| Flask-WTF | Forms & CSRF |
| Flask-Caching | Response caching |
| Flask-CORS | CORS headers |
| Flask-Limiter | Rate limiting |
| Flask-Mail | Email sending |
| Flask-RESTful | REST API framework |
| Flask-SocketIO | WebSockets |
| Flask-JWT-Extended | JWT authentication |

---

## Extension Pattern

All extensions follow the same init pattern:

```python
# Method 1: Direct init
ext = Extension(app)

# Method 2: Factory pattern (recommended)
ext = Extension()
ext.init_app(app)  # Called in create_app()
```
