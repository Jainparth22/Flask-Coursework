# Module 08 — Database | Documentation

## Overview

This module covers two approaches: raw **SQLite3** for understanding fundamentals, and **Flask-SQLAlchemy** ORM for production applications.

> 📖 **Official Docs**: [Patterns — SQLite 3](https://flask.palletsprojects.com/en/stable/patterns/sqlite3/)  
> 📖 **Flask-SQLAlchemy**: [Flask-SQLAlchemy Docs](https://flask-sqlalchemy.readthedocs.io/)

---

## Part A: Raw SQLite3

### Connection Pattern
```python
import sqlite3
from flask import g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
```

### The `g` Object
`g` is a per-request global namespace. Data stored in `g` is:
- Available throughout the request
- Unique per request (thread-safe)
- Cleared after each request

### Query Helper
```python
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv
```

> ⚠️ Always use `?` placeholders — **never** use f-strings for SQL (SQL injection!)

---

## Part B: Flask-SQLAlchemy (ORM)

### Setup
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)
```

### Defining Models
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', cascade='all, delete-orphan')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

### Column Types
| SQLAlchemy | SQL | Python |
|------------|-----|--------|
| `db.Integer` | INTEGER | `int` |
| `db.String(n)` | VARCHAR(n) | `str` |
| `db.Text` | TEXT | `str` |
| `db.Float` | FLOAT | `float` |
| `db.Boolean` | BOOLEAN | `bool` |
| `db.DateTime` | DATETIME | `datetime` |
| `db.JSON` | JSON | `dict/list` |

### CRUD Operations
```python
# CREATE
user = User(name='Alice', email='alice@example.com')
db.session.add(user)
db.session.commit()

# READ
users = User.query.all()
user = User.query.get(1)              # By primary key
user = User.query.filter_by(name='Alice').first()
users = User.query.filter(User.name.like('%li%')).all()
users = User.query.order_by(User.name.desc()).limit(10).all()

# UPDATE
user.name = 'Alice Updated'
db.session.commit()

# DELETE
db.session.delete(user)
db.session.commit()
```

### Query Methods Reference
| Method | Returns | Description |
|--------|---------|-------------|
| `.all()` | `list` | All matching records |
| `.first()` | `obj\|None` | First match or None |
| `.first_or_404()` | `obj` | First match or raise 404 |
| `.get(id)` | `obj\|None` | By primary key |
| `.count()` | `int` | Number of matches |
| `.paginate(page, per_page)` | `Pagination` | Paginated results |
| `.filter()` | `Query` | Filter with expressions |
| `.filter_by()` | `Query` | Filter with kwargs |
| `.order_by()` | `Query` | Sort results |
| `.limit(n)` | `Query` | Limit results |
| `.offset(n)` | `Query` | Skip results |

### Relationships
```python
# One-to-Many
posts = db.relationship('Post', backref='author')

# backref options:
#   lazy='select'   (default) — load when accessed
#   lazy='dynamic'  — returns query object
#   lazy='joined'   — JOIN in same query
#   lazy='subquery' — subquery in same query

# cascade options:
#   'all, delete-orphan' — delete children when parent deleted
```

---

## Key Takeaways
- Raw SQLite: Use `g` for per-request resources, `teardown_appcontext` for cleanup  
- SQLAlchemy ORM: Models = classes, queries = chained methods  
- Always use parameterized queries (never f-strings for SQL)  
- `db.session.commit()` to persist changes, `db.session.rollback()` on error
