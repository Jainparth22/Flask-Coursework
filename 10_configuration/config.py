"""
Configuration Classes
======================
Class-based config — the recommended pattern for Flask apps.
Inherit from BaseConfig, override per environment.
"""

import os


class BaseConfig:
    """Base configuration — shared across all environments."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-change-this')
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    
    # Custom app settings
    CUSTOM_APP_NAME = 'Flask Coursework'
    CUSTOM_ITEMS_PER_PAGE = 20


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_ECHO = True  # Log SQL queries


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database
    WTF_CSRF_ENABLED = False  # Disable CSRF in tests


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod.db')
    SESSION_COOKIE_SECURE = True  # HTTPS only
    # SECRET_KEY should ALWAYS come from environment in production
