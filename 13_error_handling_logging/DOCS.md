# Module 13 — Error Handling & Logging | Documentation

## Overview

Flask provides hooks for custom error pages and integrates with Python's `logging` module.

> 📖 **Official Docs**: [Handling Errors](https://flask.palletsprojects.com/en/stable/errorhandling/)  
> 📖 **Official Docs**: [Logging](https://flask.palletsprojects.com/en/stable/logging/)

---

## 1. Custom Error Handlers

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# Catch-all for unhandled exceptions
@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.exception(f'Unhandled: {error}')
    return render_template('500.html'), 500
```

## 2. Content Negotiation

```python
@app.errorhandler(404)
def not_found(error):
    if request.accept_mimetypes.accept_json:
        return jsonify({'error': 'Not found'}), 404
    return render_template('404.html'), 404
```

## 3. Logging Levels

| Level | Method | Use For |
|-------|--------|---------|
| DEBUG | `app.logger.debug()` | Development details |
| INFO | `app.logger.info()` | General operations |
| WARNING | `app.logger.warning()` | Unexpected but not fatal |
| ERROR | `app.logger.error()` | Failures |
| CRITICAL | `app.logger.critical()` | System failures |

## 4. File Logging

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=1_000_000, backupCount=10)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
app.logger.addHandler(handler)
```

## 5. Request Logging

```python
@app.before_request
def log_request():
    app.logger.debug(f'{request.method} {request.path}')

@app.after_request
def log_response(response):
    app.logger.debug(f'Response: {response.status_code}')
    return response
```

---

## Key Takeaways
- `@app.errorhandler(code)` for custom error pages
- `@app.errorhandler(Exception)` as catch-all
- `app.logger` for Flask's built-in logger
- `RotatingFileHandler` for production log files
- `before_request` / `after_request` for request logging
