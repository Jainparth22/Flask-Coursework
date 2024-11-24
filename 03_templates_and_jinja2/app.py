"""
Module 03 — Templates & Jinja2
================================
Template rendering, Jinja2 syntax: variables, filters, conditionals,
loops, template inheritance, macros, and custom filters.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, render_template
from markupsafe import Markup
from datetime import datetime

app = Flask(__name__)


# ============================================================
# 1. BASIC TEMPLATE RENDERING
# ============================================================

@app.route('/')
def index():
    """Render a template with variables passed as keyword args."""
    return render_template(
        'index.html',
        title='Home',
        message='Welcome to the Templates Module!',
        year=datetime.now().year,
    )


# ============================================================
# 2. PASSING DATA TO TEMPLATES
# ============================================================

@app.route('/about')
def about():
    """Pass complex data structures to templates."""
    team = [
        {'name': 'Alice', 'role': 'Backend Developer', 'skills': ['Python', 'Flask', 'PostgreSQL']},
        {'name': 'Bob', 'role': 'Frontend Developer', 'skills': ['JavaScript', 'React', 'CSS']},
        {'name': 'Charlie', 'role': 'DevOps Engineer', 'skills': ['Docker', 'K8s', 'AWS']},
    ]
    return render_template(
        'about.html',
        title='About Us',
        team=team,
        show_skills=True,
    )


# ============================================================
# 3. TEMPLATE WITH MACROS
# ============================================================

@app.route('/macros')
def macros_demo():
    """Demonstrate Jinja2 macros (reusable template components)."""
    fields = [
        {'name': 'username', 'label': 'Username', 'type': 'text', 'required': True},
        {'name': 'email', 'label': 'Email', 'type': 'email', 'required': True},
        {'name': 'bio', 'label': 'Bio', 'type': 'text', 'required': False},
    ]
    return render_template('macros_demo.html', title='Macros Demo', fields=fields)


# ============================================================
# 4. CUSTOM JINJA2 FILTERS
# ============================================================
# Filters transform template variables: {{ value|filter_name }}

@app.template_filter('reverse_string')
def reverse_string_filter(s):
    """Custom filter: {{ "hello"|reverse_string }} → "olleh" """
    return s[::-1]


@app.template_filter('format_date')
def format_date_filter(date_obj, fmt='%B %d, %Y'):
    """Custom filter: {{ date_obj|format_date }} → "January 01, 2025" """
    if isinstance(date_obj, str):
        date_obj = datetime.fromisoformat(date_obj)
    return date_obj.strftime(fmt)


@app.template_filter('truncate_words')
def truncate_words_filter(s, num=10):
    """Custom filter: {{ text|truncate_words(5) }} → first 5 words + ... """
    words = s.split()
    if len(words) <= num:
        return s
    return ' '.join(words[:num]) + '...'


@app.route('/filters')
def filters_demo():
    """Demonstrate built-in and custom filters."""
    return render_template(
        'filters_demo.html',
        title='Filters Demo',
        sample_text='Flask is a lightweight WSGI web application framework written in Python',
        sample_date=datetime.now(),
        sample_list=['Python', 'Flask', 'Jinja2', 'Werkzeug'],
        sample_number=1234567.89,
    )


# ============================================================
# 5. CONTEXT PROCESSORS
# ============================================================
# Make variables available to ALL templates automatically.

@app.context_processor
def inject_globals():
    """Inject variables into every template context."""
    return {
        'app_name': 'Flask Coursework',
        'current_year': datetime.now().year,
        'nav_links': [
            {'url': '/', 'label': 'Home'},
            {'url': '/about', 'label': 'About'},
            {'url': '/filters', 'label': 'Filters'},
            {'url': '/macros', 'label': 'Macros'},
        ],
    }


# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)
