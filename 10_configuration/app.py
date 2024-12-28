"""
Module 10 — Configuration & Environment Management
=====================================================
Different config approaches: dict, class-based, .env files,
instance folders, and environment-specific configs.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

import os
from flask import Flask, jsonify


# ============================================================
# METHOD 1: Direct dict-style config
# ============================================================

app = Flask(__name__, instance_relative_config=True)

# --- 1a. Directly set values ---
app.config['SECRET_KEY'] = 'fallback-secret'
app.config['DEBUG'] = True

# --- 1b. From a dict / update ---
app.config.update(
    TESTING=False,
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16 MB
    CUSTOM_SETTING='hello',
)

# --- 1c. From a Python config file ---
# app.config.from_pyfile('config.py')        # Load from config.py in root
# app.config.from_pyfile('config.py', silent=True)  # Ignore if missing

# --- 1d. From an object (class-based) ---
# app.config.from_object('config.ProductionConfig')
# app.config.from_object(config.DevelopmentConfig)

# --- 1e. From environment variable pointing to a file ---
# export FLASK_CONFIG=/path/to/config.py
# app.config.from_envvar('FLASK_CONFIG')

# --- 1f. From a .env file (via python-dotenv) ---
# pip install python-dotenv
# Create .env:  SECRET_KEY=my-secret
# Flask auto-loads .env if python-dotenv is installed

# --- 1g. From a JSON/TOML file ---
# app.config.from_file('config.json', load=json.load)
# app.config.from_file('config.toml', load=toml.load)  # Python 3.11+

# --- 1h. Load from environment variables with prefix ---
# app.config.from_prefixed_env()  # Loads FLASK_* env vars → strips FLASK_ prefix


# ============================================================
# USE CLASS-BASED CONFIG (recommended for real projects)
# ============================================================

from config import DevelopmentConfig, ProductionConfig, TestingConfig

# Choose config based on env var
config_name = os.environ.get('FLASK_ENV', 'development')
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
app.config.from_object(config_map.get(config_name, DevelopmentConfig))


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    return '''
    <h1>Module 10 — Configuration</h1>
    <ul>
        <li><a href="/config">View Current Config</a></li>
        <li><a href="/env">Environment Variables</a></li>
    </ul>
    '''

@app.route('/config')
def show_config():
    """Show non-sensitive config values."""
    safe_keys = [
        'DEBUG', 'TESTING', 'ENV', 'SECRET_KEY', 'SERVER_NAME',
        'MAX_CONTENT_LENGTH', 'SQLALCHEMY_DATABASE_URI',
        'SESSION_COOKIE_HTTPONLY', 'SESSION_COOKIE_SECURE',
    ]
    config_data = {}
    for key in sorted(app.config.keys()):
        if key in safe_keys or key.startswith('CUSTOM_'):
            value = app.config[key]
            # Mask secrets
            if 'SECRET' in key and value:
                value = value[:4] + '***'
            config_data[key] = str(value)
    return jsonify(config_data)


@app.route('/env')
def show_env():
    """Show Flask-related environment variables."""
    env_vars = {k: v for k, v in os.environ.items() if 'FLASK' in k or 'PYTHON' in k}
    return jsonify(env_vars)


if __name__ == '__main__':
    app.run()
