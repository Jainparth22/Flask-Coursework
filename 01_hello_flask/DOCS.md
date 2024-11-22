# Module 01 — Hello Flask | Documentation

## What is Flask?

Flask is a **micro web framework** for Python. "Micro" means Flask keeps the core simple but extensible — it doesn't include database abstraction, form validation, or other components by default. Instead, Flask provides the foundation and lets you choose what you need via **extensions**.

Flask is built on two key libraries:
- **Werkzeug** — A WSGI (Web Server Gateway Interface) toolkit that handles HTTP requests/responses
- **Jinja2** — A template engine for rendering HTML

> 📖 **Official Docs**: [Welcome to Flask](https://flask.palletsprojects.com/en/stable/)

---

## Core Concepts in This Module

### 1. The Flask Application Object

```python
from flask import Flask
app = Flask(__name__)
```

| Parameter | Purpose |
|-----------|---------|
| `__name__` | Tells Flask the name of the current module, so it knows where to look for templates, static files, etc. |
| `import_name` | The first argument — almost always `__name__` |
| `static_folder` | Path to the static files folder (default: `'static'`) |
| `template_folder` | Path to the templates folder (default: `'templates'`) |
| `instance_path` | Path to the instance folder for config files |

> 📖 **Official Docs**: [Flask Class API](https://flask.palletsprojects.com/en/stable/api/#flask.Flask)

---

### 2. Routes and View Functions

A **route** maps a URL to a Python function:

```python
@app.route('/')
def home():
    return 'Hello, World!'
```

**How it works**:
1. User visits `http://127.0.0.1:5000/`
2. Flask matches `/` to the `home()` function
3. `home()` runs and returns a string
4. Flask sends that string as the HTTP response body

**Dynamic Routes** use `<variable>` syntax:
```python
@app.route('/user/<name>')
def user_profile(name):
    return f'Profile of {name}'
```

> 📖 **Official Docs**: [Quickstart — A Minimal Application](https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application)

---

### 3. Running the Dev Server

#### Method A: `app.run()` (in code)
```python
if __name__ == '__main__':
    app.run(debug=True)
```

| Argument | Default | Description |
|----------|---------|-------------|
| `host` | `'127.0.0.1'` | Bind address. Use `'0.0.0.0'` for network access |
| `port` | `5000` | Port number |
| `debug` | `False` | Enable debug mode (auto-reload + debugger) |
| `use_reloader` | `True` (in debug) | Auto-restart on code changes |
| `use_debugger` | `True` (in debug) | Show interactive debugger on errors |

#### Method B: Flask CLI (recommended)
```bash
# Windows PowerShell
$env:FLASK_APP = "app"
$env:FLASK_DEBUG = "1"
flask run

# macOS/Linux
export FLASK_APP=app
export FLASK_DEBUG=1
flask run
```

> 📖 **Official Docs**: [Development Server](https://flask.palletsprojects.com/en/stable/server/)

---

### 4. Debug Mode

When `debug=True`:
- ♻️ **Auto-reloader**: Server restarts when you save code changes
- 🐛 **Interactive debugger**: Shows a traceback in the browser with a PIN-protected console
- ⚠️ **NEVER enable in production** — the debugger allows arbitrary code execution!

> 📖 **Official Docs**: [Quickstart — Debug Mode](https://flask.palletsprojects.com/en/stable/quickstart/#debug-mode)

---

## What's Happening Under the Hood?

```
Browser Request → Werkzeug (WSGI) → Flask App → Route Matching → View Function → Response
```

1. Browser sends HTTP request to `127.0.0.1:5000`
2. Werkzeug receives the raw WSGI request
3. Flask wraps it into a `Request` object
4. Flask's URL map finds the matching route
5. The view function executes and returns data
6. Flask wraps the return value into a `Response` object
7. Werkzeug sends the HTTP response back to the browser

---

## Try It Yourself

1. Run `python app.py`
2. Visit `http://127.0.0.1:5000/` → See "Hello, Flask!"
3. Visit `http://127.0.0.1:5000/about` → See the about page
4. Visit `http://127.0.0.1:5000/greet/YourName` → See personalized greeting
5. Change the return string in `home()`, save, and watch the server auto-reload

---

## Key Takeaways

- `Flask(__name__)` creates the application
- `@app.route('/path')` maps URLs to functions
- View functions return strings (or other response types, covered in Module 05)
- `app.run(debug=True)` starts the dev server with hot-reload
- Use the Flask CLI (`flask run`) for more control
