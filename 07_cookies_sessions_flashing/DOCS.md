# Module 07 — Cookies, Sessions & Message Flashing | Documentation

## Overview

HTTP is stateless — cookies and sessions add statefulness. Cookies are raw browser storage; Flask sessions are tamper-proof signed cookies.

> 📖 **Official Docs**: [Quickstart — Cookies](https://flask.palletsprojects.com/en/stable/quickstart/#cookies)  
> 📖 **Official Docs**: [Quickstart — Sessions](https://flask.palletsprojects.com/en/stable/quickstart/#sessions)

---

## 1. Cookies

### Setting Cookies
```python
from flask import make_response

resp = make_response('Cookie set!')
resp.set_cookie('key', 'value',
    max_age=3600,         # Seconds until expiry (None = session cookie)
    httponly=True,         # Not accessible via JavaScript (XSS protection)
    secure=True,           # Only sent over HTTPS  
    samesite='Lax',        # CSRF protection: 'Strict' | 'Lax' | 'None'
    path='/',              # Cookie applies to this URL path
    domain=None,           # Cookie domain (None = current domain)
)
```

### Cookie Options Explained

| Option | Description | Recommended |
|--------|-------------|-------------|
| `max_age` | Lifetime in seconds. `None` = browser session | Set explicitly |
| `httponly` | Block `document.cookie` access | `True` always |
| `secure` | HTTPS only | `True` in production |
| `samesite` | When cookie is sent cross-site | `'Lax'` or `'Strict'` |
| `path` | URL scope | `'/'` |
| `domain` | Domain scope | `None` (current domain) |

### Reading Cookies
```python
value = request.cookies.get('key', 'default')
all_cookies = request.cookies.to_dict()
```

### Deleting Cookies
```python
resp.delete_cookie('key')  # Alias for set_cookie with max_age=0
```

---

## 2. Sessions

Flask sessions are **signed cookies** — the data is visible to users (base64 + JSON) but **cannot be tampered with** because it's cryptographically signed with `SECRET_KEY`.

### Setup
```python
app.config['SECRET_KEY'] = 'your-secret-key'  # REQUIRED
```

### Using Sessions
```python
from flask import session

# Set
session['username'] = 'parth'
session['items'] = [1, 2, 3]

# Get
name = session.get('username', 'Guest')
name = session['username']  # KeyError if missing

# Check
if 'username' in session:
    ...

# Delete one key
session.pop('username', None)

# Clear all
session.clear()

# Mark as modified (needed for mutable nested objects)
session.modified = True
```

### Permanent Sessions
```python
from datetime import timedelta

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# In a view:
session.permanent = True  # Uses PERMANENT_SESSION_LIFETIME instead of browser session
```

### Session vs Cookies

| Feature | Cookies | Sessions |
|---------|---------|----------|
| Storage | Client (browser) | Client (signed cookie) |
| Tamper-proof | ❌ No | ✅ Yes (signed) |
| Size limit | ~4KB | ~4KB |
| Encryption | ❌ No | ❌ No (only signed) |
| Auto-serialization | Manual | JSON (automatic) |
| Setup needed | None | `SECRET_KEY` required |

> 📖 **Official Docs**: [Sessions](https://flask.palletsprojects.com/en/stable/quickstart/#sessions)

---

## 3. Message Flashing

Flash messages are one-time messages stored in the session, displayed on the **next** page load, then automatically cleared.

### In Python
```python
from flask import flash

flash('Account created!', 'success')      # With category
flash('Check your email.', 'info')
flash('Invalid password.', 'error')
flash('Uncategorized message')            # Category defaults to 'message'
```

### In Templates
```html
{# Without categories #}
{% for message in get_flashed_messages() %}
    <div class="alert">{{ message }}</div>
{% endfor %}

{# With categories (recommended) #}
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}

{# Filter by category #}
{% for message in get_flashed_messages(category_filter=["error"]) %}
    <div class="error">{{ message }}</div>
{% endfor %}
```

> 📖 **Official Docs**: [Message Flashing](https://flask.palletsprojects.com/en/stable/quickstart/#message-flashing)

---

## Key Takeaways

- **Cookies**: Raw key-value storage in the browser; use `httponly`, `secure`, `samesite`
- **Sessions**: Signed cookies (tamper-proof); requires `SECRET_KEY`
- **Flash**: One-time messages via session; `flash()` + `get_flashed_messages()`
- Sessions are NOT encrypted — don't store secrets in them
- For server-side sessions, use Flask-Session extension
