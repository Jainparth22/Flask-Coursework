"""
Module 01 — Hello Flask
========================
The absolute basics of Flask: creating an app, defining routes,
and running the development server.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask

# ============================================================
# 1. CREATING A FLASK APPLICATION INSTANCE
# ============================================================
# The Flask class is the core of every Flask application.
# __name__ tells Flask where to find templates, static files, etc.
# It resolves to the name of the current Python module.

app = Flask(__name__)


# ============================================================
# 2. DEFINING ROUTES WITH DECORATORS
# ============================================================
# @app.route() maps a URL path to a Python function (a "view function").
# When a user visits that URL, Flask calls this function
# and sends its return value as the HTTP response.

@app.route('/')
def home():
    """The simplest possible route — returns a plain string."""
    return '<h1>Hello, Flask! 🚀</h1><p>Welcome to Module 01.</p>'


@app.route('/about')
def about():
    """Another route at /about."""
    return '<h1>About</h1><p>This is a Flask coursework project.</p>'


@app.route('/greet/<name>')
def greet(name):
    """Dynamic route — captures a URL segment as a variable.
    
    Visit: /greet/Parth → "Hello, Parth!"
    """
    return f'<h1>Hello, {name}!</h1>'


# ============================================================
# 3. RUNNING THE APPLICATION
# ============================================================
# app.run() starts Flask's built-in development server.
#
# Parameters:
#   debug=True   → Auto-reload on code changes + interactive debugger
#   host='0.0.0.0' → Make server accessible on the network
#   port=5000    → Port number (default is 5000)
#
# IMPORTANT: Never use app.run() in production!
# Use a production WSGI server like Gunicorn instead (see Module 19).

if __name__ == '__main__':
    app.run(debug=True)


# ============================================================
# ALTERNATIVE: Running with the Flask CLI
# ============================================================
# Instead of app.run(), you can use the command line:
#
#   # Set the app module (Windows PowerShell)
#   $env:FLASK_APP = "app"
#
#   # Enable debug mode
#   $env:FLASK_DEBUG = "1"
#
#   # Run
#   flask run
#
# This is the recommended way for development.
# ============================================================
