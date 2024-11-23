# Module 02 — Routing & URL Building | Documentation

## Overview

Routing is how Flask maps URLs to Python functions. Every web application needs to define what happens when a user visits a specific URL — that's what routing does.

> 📖 **Official Docs**: [Quickstart — Routing](https://flask.palletsprojects.com/en/stable/quickstart/#routing)

---

## 1. Basic Routes

```python
@app.route('/')
def index():
    return 'Hello!'
```

The `@app.route()` decorator registers a **URL rule** that maps a path to a **view function**. Internally, Flask uses `app.add_url_rule()`:

```python
# These two are equivalent:
@app.route('/')
def index():
    return 'Hello!'

def index():
    return 'Hello!'
app.add_url_rule('/', 'index', index)
```

> 📖 **Official Docs**: [URL Route Registrations](https://flask.palletsprojects.com/en/stable/api/#url-route-registrations)

---

## 2. Variable Rules (Dynamic Routes)

Capture parts of the URL as function arguments:

```python
@app.route('/user/<username>')
def profile(username):
    return f'User: {username}'
```

### URL Converters

| Converter | Accepts | Example Route | Example URL | Python Type |
|-----------|---------|---------------|-------------|-------------|
| `string` | Text without `/` (default) | `/<username>` | `/parth` | `str` |
| `int` | Positive integers | `/<int:id>` | `/42` | `int` |
| `float` | Positive floats | `/<float:price>` | `/9.99` | `float` |
| `path` | Text including `/` | `/<path:filepath>` | `/docs/api/v2` | `str` |
| `uuid` | UUID strings | `/<uuid:id>` | `/550e8400-...` | `uuid.UUID` |

> 📖 **Official Docs**: [Variable Rules](https://flask.palletsprojects.com/en/stable/quickstart/#variable-rules)

---

## 3. Trailing Slash Behavior

Flask treats trailing slashes precisely:

| Route Definition | Visit `/path` | Visit `/path/` |
|------------------|---------------|-----------------|
| `@app.route('/path/')` | 301 redirect → `/path/` | ✅ Works |
| `@app.route('/path')` | ✅ Works | ❌ 404 Not Found |

**Rule of thumb**: 
- Use trailing slash (`/path/`) for "folder-like" endpoints (lists, collections)
- Use no trailing slash (`/path`) for "file-like" endpoints (specific resources)

> 📖 **Official Docs**: [Unique URLs / Redirection Behavior](https://flask.palletsprojects.com/en/stable/quickstart/#unique-urls-redirection-behavior)

---

## 4. URL Building with `url_for()`

`url_for()` generates a URL for a given view **function name** (not the URL path):

```python
from flask import url_for

url_for('index')                              # → '/'
url_for('user_profile', username='parth')     # → '/user/parth'
url_for('show_post', post_id=42)              # → '/post/42'
url_for('index', page=2, sort='name')         # → '/?page=2&sort=name'
url_for('static', filename='style.css')       # → '/static/style.css'
```

### Why use `url_for()` instead of hardcoding?

1. **Descriptive** — Function names are more meaningful than URLs
2. **Maintainable** — Change a URL in one place, all references update
3. **Escaping** — Handles special characters automatically
4. **External URLs** — `url_for('index', _external=True)` → `http://127.0.0.1:5000/`
5. **Query Strings** — Extra keyword args become `?key=value` parameters

> 📖 **Official Docs**: [URL Building](https://flask.palletsprojects.com/en/stable/quickstart/#url-building)

---

## 5. HTTP Methods

By default, routes only accept **GET** requests. Use `methods` to accept others:

```python
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Handle form submission
        return 'Data received!'
    return '<form method="POST">...</form>'
```

### Common HTTP Methods

| Method | Purpose | Idempotent? | Safe? |
|--------|---------|-------------|-------|
| `GET` | Read / Retrieve data | ✅ | ✅ |
| `POST` | Create new resource | ❌ | ❌ |
| `PUT` | Replace/update resource | ✅ | ❌ |
| `PATCH` | Partially update resource | ❌ | ❌ |
| `DELETE` | Delete resource | ✅ | ❌ |
| `HEAD` | Like GET but no body | ✅ | ✅ |
| `OPTIONS` | Get allowed methods | ✅ | ✅ |

> **Idempotent**: Same request repeated → same result  
> **Safe**: Doesn't modify server state

> 📖 **Official Docs**: [HTTP Methods](https://flask.palletsprojects.com/en/stable/quickstart/#http-methods)

---

## 6. Multiple Routes → One Function

Stack decorators for aliases:

```python
@app.route('/page')
@app.route('/page/<int:num>')
def paginated(num=1):
    return f'Page {num}'
```

---

## 7. Redirects

```python
from flask import redirect, url_for

@app.route('/old-url')
def old_url():
    return redirect(url_for('new_url'))
```

The default redirect status is **302 (Found)**. For permanent redirects, use:
```python
return redirect(url_for('new_url'), code=301)
```

---

## Key Takeaways

- `@app.route('/path')` maps a URL to a view function
- Variable rules (`<int:id>`) capture URL segments as typed arguments
- `url_for('function_name')` builds URLs from function names — **always prefer this**
- Trailing slashes matter: `/path/` redirects, `/path` gives 404 on `/path/`
- Use `methods=['GET', 'POST']` to accept different HTTP methods
- `request.method` tells you how the current request was made
