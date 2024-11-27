"""
Module 04 — Static Files & Project Layout
==========================================
Serving CSS, JavaScript, images, and understanding
Flask's recommended project structure.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    """Homepage with CSS styled via static files."""
    return render_template('index.html', title='Static Files Demo')


@app.route('/layout')
def layout_info():
    """Show Flask project layout conventions."""
    layouts = {
        'Simple (Single File)': '''
project/
├── app.py
├── templates/
│   └── index.html
└── static/
    ├── style.css
    ├── script.js
    └── images/
        └── logo.png
        ''',
        'Medium (Modular)': '''
project/
├── app.py
├── config.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   └── about.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
│       └── logo.png
└── tests/
    └── test_app.py
        ''',
        'Large (Application Factory)': '''
project/
├── run.py
├── config.py
├── requirements.txt
├── myapp/
│   ├── __init__.py        ← create_app() factory
│   ├── models.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/auth/
│   │       └── login.html
│   ├── main/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/main/
│   │       └── index.html
│   ├── templates/
│   │   └── base.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
└── tests/
    ├── conftest.py
    └── test_auth.py
        ''',
    }
    return render_template('layout.html', title='Project Layouts', layouts=layouts)


if __name__ == '__main__':
    app.run(debug=True)
