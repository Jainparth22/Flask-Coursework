# Module 20 — Capstone: Blog Application | Documentation

## Overview

This module ties together **everything** from Modules 01-19 into a production-style blog application.

---

## Concepts Used

| Concept | Module | Where Used |
|---------|--------|------------|
| Application Factory | 09 | `blog/__init__.py` → `create_app()` |
| Blueprints | 09 | `main`, `auth`, `posts` blueprints |
| Configuration | 10 | Environment-based config in factory |
| SQLAlchemy Models | 08 | `User` and `Post` with relationships |
| Flask-Login | 11 | Authentication, `@login_required` |
| Password Hashing | 11 | `werkzeug.security` |
| Templates | 03 | Jinja2 inheritance (`base.html`) |
| Flash Messages | 07 | Success/error feedback |
| Static Files | 04 | Inline CSS (upgradeable) |
| Error Handling | 13 | Custom 404 handler |
| Request/Response | 05 | Form handling, redirects |

---

## How to Run

```bash
cd 20_capstone_blog
pip install flask flask-sqlalchemy flask-login
python run.py
# Visit http://127.0.0.1:5000
```

## Structure

```
20_capstone_blog/
├── run.py                     ← Entry point
└── blog/
    ├── __init__.py            ← create_app() factory
    ├── extensions.py          ← db, login_manager
    ├── models.py              ← User, Post models
    ├── main.py                ← Homepage blueprint
    ├── auth.py                ← Register/Login/Logout
    ├── posts.py               ← CRUD posts
    └── templates/
        ├── base.html          ← Layout
        ├── index.html         ← Post listing
        ├── auth/login.html
        ├── auth/register.html
        ├── posts/new.html
        ├── posts/view.html
        └── posts/edit.html
```

---

## Next Steps (extend yourself!)
- Add pagination to the homepage
- Add user profiles
- Add comments on posts
- Add tags/categories
- Add search
- Deploy with Gunicorn + Nginx
