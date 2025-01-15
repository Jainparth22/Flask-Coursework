# Module 15 — Middleware, Hooks & Signals | Documentation

## Overview

Flask provides hooks to run code at specific points in the request lifecycle, plus a signal system for decoupled event handling.

> 📖 **Official Docs**: [Request Lifecycle](https://flask.palletsprojects.com/en/stable/lifecycle/)  
> 📖 **Official Docs**: [Signals](https://flask.palletsprojects.com/en/stable/signals/)

---

## 1. Request Hooks

```
Client → WSGI Middleware → before_request → View → after_request → teardown_request → Response
```

### `@app.before_request`
```python
@app.before_request
def before():
    g.start_time = time()
    # Return a response to short-circuit (skip view)
```

### `@app.after_request`
```python
@app.after_request
def after(response):
    response.headers['X-Custom'] = 'value'
    return response  # MUST return response
```

### `@app.teardown_request`
```python
@app.teardown_request
def teardown(exception):
    # Always runs, even on error. Cleanup here.
    db.close()
```

### Blueprint-level Hooks
```python
@blueprint.before_request      # Only for this blueprint's routes
@blueprint.after_request
@blueprint.before_app_request   # For ALL routes (registered via blueprint)
```

---

## 2. Signals (blinker)

Signals are observer-pattern events. They don't modify behavior — they notify.

### Built-in Signals
| Signal | Fires When |
|--------|-----------|
| `request_started` | Request begins |
| `request_finished` | Request ends |
| `got_request_exception` | Unhandled exception |
| `template_rendered` | Template rendered |
| `before_render_template` | Before template render |

```python
from flask import request_finished

def on_finished(sender, response, **kwargs):
    print(f'Response: {response.status_code}')

request_finished.connect(on_finished, app)
```

### Custom Signals
```python
from blinker import Namespace
my_signals = Namespace()
user_logged_in = my_signals.signal('user-logged-in')

# Emit
user_logged_in.send(app, user='parth')

# Handle
user_logged_in.connect(lambda sender, user: print(f'{user} logged in'))
```

---

## 3. WSGI Middleware

```python
class MyMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        # Pre-processing
        return self.app(environ, start_response)

app.wsgi_app = MyMiddleware(app.wsgi_app)
```

---

## Hooks vs Signals
| Feature | Hooks | Signals |
|---------|-------|---------|
| Can modify request/response | ✅ Yes | ❌ No |
| Can short-circuit request | ✅ Yes | ❌ No |
| Decoupled | ❌ No | ✅ Yes |
| Multiple subscribers | Ordered | Unordered |
| Use case | Auth, headers, logging | Analytics, notifications |

---

## Key Takeaways
- `before_request` for auth/setup, `after_request` for headers, `teardown_request` for cleanup
- Hooks can modify behavior; signals are for observation only
- WSGI middleware is the lowest level (before Flask processes request)
