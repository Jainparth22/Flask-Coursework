# Module 04 — Static Files & Project Layout | Documentation

## Overview

Flask automatically serves files from the `static/` folder in your project. These are files that don't change per-request — CSS stylesheets, JavaScript files, images, fonts, etc.

> 📖 **Official Docs**: [Quickstart — Static Files](https://flask.palletsprojects.com/en/stable/quickstart/#static-files)

---

## 1. The `static/` Folder

By default, Flask serves static files from a `static/` directory next to your `app.py`:

```
project/
├── app.py
└── static/
    ├── style.css
    ├── script.js
    └── images/
        └── logo.png
```

Files are accessible at `/static/<filename>`:
- `static/style.css` → `http://127.0.0.1:5000/static/style.css`

---

## 2. Referencing Static Files in Templates

**Always use `url_for()`** — never hardcode paths:

```html
<!-- CSS -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

<!-- JavaScript -->
<script src="{{ url_for('static', filename='js/app.js') }}"></script>

<!-- Images -->
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">

<!-- Favicon -->
<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
```

### Why `url_for('static', ...)` over hardcoding?
| Hardcoded | `url_for()` |
|-----------|-------------|
| `/static/style.css` | `{{ url_for('static', filename='style.css') }}` |
| Breaks if app is mounted at a subdirectory | Always correct |
| No cache busting | URL changes with modifications |
| Blueprint-unaware | Resolves per-blueprint static folders |

---

## 3. Customizing the Static Folder

```python
# Change the folder name
app = Flask(__name__, static_folder='assets')
# Now files are served from assets/ instead of static/

# Change the URL path
app = Flask(__name__, static_url_path='/cdn')
# Now files are at /cdn/style.css instead of /static/style.css

# Disable static file serving entirely
app = Flask(__name__, static_folder=None)
```

---

## 4. Project Layout Patterns

### Simple (Learning / Scripts)
```
project/
├── app.py
├── templates/
│   └── index.html
└── static/
    └── style.css
```

### Medium (Small Applications)
```
project/
├── app.py
├── config.py
├── models.py
├── forms.py
├── requirements.txt
├── templates/
│   ├── base.html
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── tests/
    └── test_app.py
```

### Large (Application Factory + Blueprints)
```
project/
├── run.py              ← Entry point
├── config.py           ← Configuration classes
├── requirements.txt
├── myapp/
│   ├── __init__.py     ← create_app() factory
│   ├── models.py       ← Database models
│   ├── extensions.py   ← Extension instances
│   ├── auth/           ← Auth blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/auth/
│   ├── main/           ← Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/      ← Shared templates
│   │   └── base.html
│   └── static/         ← Shared static files
└── tests/
```

> 📖 **Official Docs**: [Patterns — Large Applications as Packages](https://flask.palletsprojects.com/en/stable/patterns/packages/)

---

## Key Takeaways

- Static files go in `static/` folder (CSS, JS, images)
- Use `url_for('static', filename='...')` to reference them in templates
- Customize with `static_folder` and `static_url_path` parameters
- Choose project layout based on app complexity
- Blueprints can have their own `static/` and `templates/` folders
