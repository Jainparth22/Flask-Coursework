"""
Blog Application Factory
==========================
Ties together all concepts from the coursework.
"""

import os
from flask import Flask
from blog.extensions import db, login_manager
from blog.models import User


def create_app(config=None):
    app = Flask(__name__)
    
    # --- Configuration ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'capstone-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if config:
        app.config.update(config)
    
    # --- Extensions ---
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # --- Blueprints ---
    from blog.main import main_bp
    from blog.auth import auth_bp
    from blog.posts import posts_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(posts_bp, url_prefix='/posts')
    
    # --- Error Handlers ---
    @app.errorhandler(404)
    def not_found(e):
        return '<h1>404 — Page Not Found</h1><a href="/">← Home</a>', 404
    
    # --- Create tables ---
    with app.app_context():
        db.create_all()
    
    return app
