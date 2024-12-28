# Module 10 — Configuration & Environment Management | Documentation

## Overview

Flask applications use `app.config` — a dict subclass — to store all configuration. Flask supports many ways to load config values.

> 📖 **Official Docs**: [Configuration Handling](https://flask.palletsprojects.com/en/stable/config/)

---

## 1. Loading Configuration

### Direct Assignment
```python
app.config['SECRET_KEY'] = 'my-secret'
app.config.update(DEBUG=True, TESTING=False)
```

### From a Python File
```python
app.config.from_pyfile('config.py')           # Raises error if missing
app.config.from_pyfile('config.py', silent=True)  # Ignores if missing
```

### From a Class (Recommended)
```python
class ProductionConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

app.config.from_object(ProductionConfig)
# OR by string:
app.config.from_object('config.ProductionConfig')
```

### From Environment Variable
```python
# Points to a config file path
app.config.from_envvar('FLASK_CONFIG')
```

### From .env File (python-dotenv)
```bash
pip install python-dotenv
```
```env
# .env
SECRET_KEY=my-secret
DATABASE_URL=sqlite:///app.db
```
Flask auto-loads `.env` and `.flaskenv` if python-dotenv is installed.

### From JSON/TOML
```python
import json
app.config.from_file('config.json', load=json.load)
```

### From Prefixed Env Vars
```python
app.config.from_prefixed_env()
# FLASK_SECRET_KEY=x → app.config['SECRET_KEY'] = 'x'
```

---

## 2. Class-Based Config Pattern

```python
class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
```

---

## 3. Built-in Config Keys

| Key | Default | Description |
|-----|---------|-------------|
| `DEBUG` | `False` | Enable debug mode |
| `TESTING` | `False` | Enable testing mode |
| `SECRET_KEY` | `None` | Signing key (sessions, CSRF) |
| `SERVER_NAME` | `None` | Host:port for URL generation |
| `MAX_CONTENT_LENGTH` | `None` | Max upload size (bytes) |
| `SESSION_COOKIE_HTTPONLY` | `True` | Block JS access to session cookie |
| `SESSION_COOKIE_SECURE` | `False` | Session cookie requires HTTPS |
| `SESSION_COOKIE_SAMESITE` | `None` | SameSite cookie attribute |
| `PERMANENT_SESSION_LIFETIME` | 31 days | Max session age |
| `PREFERRED_URL_SCHEME` | `'http'` | URL scheme for `url_for` |

---

## 4. Instance Folder

```python
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')  # Loads from instance/config.py
```

The `instance/` folder is for deployment-specific configs (database URLs, secrets) that shouldn't be in version control. Add `instance/` to `.gitignore`.

---

## Key Takeaways
- Use class-based config with inheritance (Base → Dev/Test/Prod)
- Never hardcode secrets — use `os.environ.get()`
- `.env` files + python-dotenv for local development
- `app.config.from_object()` for class-based loading
- `instance/` folder for deployment-specific secrets
