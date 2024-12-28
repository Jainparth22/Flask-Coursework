# 🧪 Flask Coursework — From Fundamentals to Production

A comprehensive, hands-on Flask learning path structured in **20 progressive modules**.  
Each module contains **runnable Python code** and a **DOCS.md** explaining every concept with references to the [official Flask 3.1.x documentation](https://flask.palletsprojects.com/en/stable/).

---

## 📋 Prerequisites

- Python 3.10+
- Basic Python knowledge (functions, classes, decorators)
- A code editor (VS Code recommended)

## 🚀 Quick Start

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Run any module
cd 01_hello_flask
python app.py
# Visit http://127.0.0.1:5000
```

---

## 📚 Course Modules

### Phase 1 — Fundamentals (Beginner)

| #  | Module | Key Concepts |
|----|--------|--------------|
| 01 | [Hello Flask](./01_hello_flask/) | Minimal app, `app.run()`, debug mode |
| 02 | [Routing & URLs](./02_routing_and_urls/) | Routes, variable rules, `url_for()`, HTTP methods |
| 03 | [Templates & Jinja2](./03_templates_and_jinja2/) | `render_template()`, inheritance, filters, macros |
| 04 | [Static Files](./04_static_files/) | Serving CSS/JS/images, project layout |
| 05 | [Request & Response](./05_request_and_response/) | `request` object, cookies, `jsonify()`, `redirect()`, `abort()` |

### Phase 2 — Intermediate

| #  | Module | Key Concepts |
|----|--------|--------------|
| 06 | [Forms & Validation](./06_forms_and_validation/) | Flask-WTF, CSRF, validators, file uploads |
| 07 | [Cookies, Sessions & Flashing](./07_cookies_sessions_flashing/) | Cookies, `session`, `flash()`, categories |
| 08 | [Database](./08_database/) | Raw SQLite, Flask-SQLAlchemy, Flask-Migrate |
| 09 | [Blueprints & Factory](./09_blueprints_and_factory/) | Blueprints, `create_app()`, modular structure |
| 10 | [Configuration](./10_configuration/) | Config classes, env vars, instance folders |

---

## 📖 Official References

- [Flask Documentation (3.1.x)](https://flask.palletsprojects.com/en/stable/)
- [Jinja2 Template Engine](https://jinja.palletsprojects.com/en/stable/)
- [Werkzeug WSGI Toolkit](https://werkzeug.palletsprojects.com/en/stable/)
- [Flask Extensions Registry](https://flask.palletsprojects.com/en/stable/extensions/)

