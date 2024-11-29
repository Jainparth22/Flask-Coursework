# Module 05 — Request & Response | Documentation

## Overview

Every Flask view function receives a **request** and must return a **response**. Understanding these two objects is fundamental to building any Flask application.

> 📖 **Official Docs**: [Quickstart — Accessing Request Data](https://flask.palletsprojects.com/en/stable/quickstart/#accessing-request-data)

---

## 1. The `request` Object

`request` is a global proxy to the current HTTP request. Import it from Flask:

```python
from flask import request
```

### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `request.method` | `str` | HTTP method: `'GET'`, `'POST'`, etc. |
| `request.url` | `str` | Full URL including query string |
| `request.base_url` | `str` | URL without query string |
| `request.path` | `str` | URL path (e.g., `/users/42`) |
| `request.host` | `str` | Host with port (e.g., `127.0.0.1:5000`) |
| `request.scheme` | `str` | `'http'` or `'https'` |
| `request.remote_addr` | `str` | Client IP address |
| `request.content_type` | `str` | MIME type of request body |
| `request.is_json` | `bool` | True if Content-Type is JSON |
| `request.user_agent` | `UserAgent` | Parsed User-Agent header |
| `request.referrer` | `str\|None` | Referring URL |

### Data Access

| Property | Data Source | Content-Type |
|----------|------------|--------------|
| `request.args` | URL query string `?key=value` | Any |
| `request.form` | POST body | `application/x-www-form-urlencoded` or `multipart/form-data` |
| `request.json` | POST body | `application/json` |
| `request.data` | Raw body bytes | Any |
| `request.files` | Uploaded files | `multipart/form-data` |
| `request.cookies` | Cookie header | Any |
| `request.headers` | HTTP headers | Any |

### ImmutableMultiDict Methods

`request.args`, `request.form`, and `request.files` are all `ImmutableMultiDict`:

```python
request.args.get('key')                    # Returns None if missing
request.args.get('key', 'default')         # With default value
request.args.get('page', 1, type=int)      # With type conversion
request.args.getlist('tags')               # Multiple values for same key
request.args.to_dict()                     # Convert to regular dict
request.args.to_dict(flat=False)           # Preserve multiple values
```

> 📖 **Official Docs**: [Request Object](https://flask.palletsprojects.com/en/stable/quickstart/#the-request-object)

---

## 2. Building Responses

Flask can return responses in several ways:

### Method 1: Return a String
```python
@app.route('/')
def index():
    return 'Hello!'  # 200 OK, text/html
```

### Method 2: Return a Tuple
```python
return 'Created!', 201                           # (body, status)
return 'OK', {'X-Custom': 'value'}               # (body, headers)
return 'Created!', 201, {'X-Custom': 'value'}    # (body, status, headers)
```

### Method 3: `make_response()`
```python
from flask import make_response

resp = make_response('Hello!')
resp.status_code = 200
resp.headers['X-Custom'] = 'value'
resp.set_cookie('user', 'parth')
return resp
```

### Method 4: Return a Dict (auto-JSON)
```python
return {'key': 'value'}  # Flask auto-calls jsonify()
```

### Method 5: `jsonify()`
```python
from flask import jsonify
return jsonify(name='Parth', age=25)  # Sets Content-Type: application/json
```

> 📖 **Official Docs**: [About Responses](https://flask.palletsprojects.com/en/stable/quickstart/#about-responses)

---

## 3. JSON APIs

```python
# Using jsonify (explicit)
@app.route('/api/user')
def get_user():
    return jsonify({'name': 'Parth', 'age': 25})

# Using dict (implicit, Flask 1.0+)
@app.route('/api/user2')
def get_user2():
    return {'name': 'Parth', 'age': 25}

# With status code
@app.route('/api/create', methods=['POST'])
def create():
    return jsonify({'created': True}), 201
```

> 📖 **Official Docs**: [APIs with JSON](https://flask.palletsprojects.com/en/stable/quickstart/#apis-with-json)

---

## 4. Cookies

### Setting Cookies
```python
resp = make_response('Cookie set!')
resp.set_cookie('key', 'value',
    max_age=3600,       # Seconds until expiry
    httponly=True,       # Block JavaScript access
    secure=True,         # HTTPS only
    samesite='Lax',      # CSRF protection: Strict/Lax/None
    domain=None,         # Cookie domain
    path='/',            # Cookie path
)
```

### Reading Cookies
```python
value = request.cookies.get('key', 'default')
```

### Deleting Cookies
```python
resp.delete_cookie('key')  # Sets max_age=0
```

> 📖 **Official Docs**: [Cookies](https://flask.palletsprojects.com/en/stable/quickstart/#cookies)

---

## 5. Redirects

```python
from flask import redirect, url_for

@app.route('/old')
def old_page():
    return redirect(url_for('new_page'))           # 302 (temporary)
    return redirect(url_for('new_page'), code=301) # 301 (permanent)
    return redirect('https://example.com')         # External URL
```

| Code | Meaning | Use Case |
|------|---------|----------|
| 301 | Moved Permanently | URL changed forever, search engines update |
| 302 | Found (Temporary) | Default, URL might change back |
| 303 | See Other | Redirect after POST (PRG pattern) |
| 307 | Temporary Redirect | Preserves HTTP method |

> 📖 **Official Docs**: [Redirects and Errors](https://flask.palletsprojects.com/en/stable/quickstart/#redirects-and-errors)

---

## 6. Error Responses with `abort()`

```python
from flask import abort

@app.route('/admin')
def admin():
    if not is_admin():
        abort(403)  # Raises HTTPException

# Custom error handler
@app.errorhandler(404)
def not_found(error):
    return '<h1>404</h1>', 404
```

| Code | Meaning |
|------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 500 | Internal Server Error |

---

## Key Takeaways

- `request.args` for query params, `request.form` for POST data, `request.json` for JSON
- Use `.get('key', default)` to avoid `KeyError`
- `jsonify()` or return a `dict` for JSON APIs
- `make_response()` for full control over headers, cookies, status
- `redirect(url_for('func'))` for redirections
- `abort(code)` to raise HTTP errors
- `@app.errorhandler(code)` to customize error pages
