# Module 09 — Blueprints & Application Factory | Documentation

## Overview

Blueprints organize a Flask application into modular components. The Application Factory pattern creates the app in a function rather than at module level.

> 📖 **Official Docs**: [Blueprints and Views](https://flask.palletsprojects.com/en/stable/tutorial/views/)  
> 📖 **Official Docs**: [Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)

---

## 1. Blueprints

A Blueprint is a reusable application component with its own routes, templates, and static files.

### Creating a Blueprint
```python
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, 
    template_folder='templates',  # Blueprint-specific templates
    static_folder='static',      # Blueprint-specific static files
    url_prefix='/auth',           # All routes prefixed with /auth
)

@auth_bp.route('/login')  # → /auth/login
def login():
    return 'Login page'
```

### Registering in the App
```python
from myapp.auth import auth_bp
app.register_blueprint(auth_bp)
# OR with prefix:
app.register_blueprint(auth_bp, url_prefix='/auth')
```

### Blueprint Parameters
| Parameter | Description |
|-----------|-------------|
| `name` | Blueprint identifier (used in `url_for`) |
| `import_name` | Usually `__name__` |
| `template_folder` | Path to blueprint templates |
| `static_folder` | Path to blueprint static files |
| `url_prefix` | URL prefix for all routes |

### `url_for` with Blueprints
```python
url_for('auth.login')   # → /auth/login
url_for('main.index')   # → /
url_for('.index')        # → current blueprint's index (shorthand)
```

---

## 2. Application Factory

```python
def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Config
    app.config.from_object(config[config_name])
    
    # Extensions
    db.init_app(app)
    
    # Blueprints
    from myapp.main import main_bp
    from myapp.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app
```

### Benefits
1. **Testing**: Create app with test config
2. **Multiple instances**: Different configs per instance
3. **No circular imports**: App created at runtime
4. **Cleaner structure**: All setup in one place

---

## 3. Project Structure

```
project/
├── run.py                 ← Entry point
├── myapp/
│   ├── __init__.py        ← create_app() factory
│   ├── auth/
│   │   ├── __init__.py    ← auth_bp = Blueprint(...)
│   │   ├── routes.py      ← @auth_bp.route(...)
│   │   └── templates/auth/
│   │       └── login.html
│   └── main/
│       ├── __init__.py    ← main_bp = Blueprint(...)
│       ├── routes.py
│       └── templates/main/
│           └── index.html
```

### Why `templates/auth/` subdirectory?
Flask searches all template folders. Without subdirectories, `login.html` in auth/ could conflict with `login.html` in main/. Namespacing prevents this.

---

## Key Takeaways
- Blueprints = modular components with their own routes/templates/static
- `url_for('blueprint.view')` for cross-blueprint links
- Factory pattern = `create_app()` function for flexible app creation
- Import routes AFTER creating the blueprint to avoid circular imports
- Use `url_prefix` to namespace blueprint URLs
