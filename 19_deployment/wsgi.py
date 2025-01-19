"""
Module 19 — Deployment Configuration
=======================================
Production-ready configuration files and entry points.
"""

import os


# ============================================================
# 1. PRODUCTION ENTRY POINT (wsgi.py)
# ============================================================

# This file is used by WSGI servers (Gunicorn, Waitress)
# Command: gunicorn -w 4 wsgi:app

def create_app():
    """Application factory for production."""
    from flask import Flask
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me')
    app.config['DEBUG'] = False
    
    @app.route('/')
    def index():
        return {'status': 'running', 'env': 'production'}
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run()
