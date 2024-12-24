"""
Application Factory — create_app()
====================================
The factory pattern lets you create multiple app instances
with different configurations (testing, development, production).
"""

from flask import Flask


def create_app(config_name='development'):
    """Application Factory function.
    
    Why use a factory?
    1. Testing — create app with test config
    2. Multiple instances — run different configs
    3. No circular imports — app created at runtime, not import time
    4. Blueprints registered inside factory
    """
    app = Flask(__name__)
    
    # ---- CONFIGURATION ----
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret'
    else:
        app.config['SECRET_KEY'] = 'dev-secret-change-this'
        app.config['DEBUG'] = True
    
    # ---- REGISTER BLUEPRINTS ----
    from myapp.main import main_bp
    from myapp.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    #                      ^^^^^^^^^^^^^^^^^^^^^^^^^^
    # url_prefix makes all auth routes start with /auth/
    # So /login becomes /auth/login
    
    # ---- ERROR HANDLERS ----
    @app.errorhandler(404)
    def not_found(e):
        return '<h1>404 — Not Found</h1><a href="/">← Home</a>', 404
    
    return app
