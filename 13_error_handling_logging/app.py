"""
Module 13 — Error Handling & Logging
=======================================
Custom error pages, exception handling, Flask's logging system,
and structured logging for production.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


# ============================================================
# 1. CUSTOM ERROR HANDLERS
# ============================================================

@app.errorhandler(400)
def bad_request(error):
    """400 Bad Request."""
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400
    return render_template('error.html', code=400, message='Bad Request'), 400


@app.errorhandler(404)
def not_found(error):
    """404 Page Not Found."""
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Not Found'}), 404
    return render_template('error.html', code=404, message='Page Not Found'), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', code=403, message='Forbidden'), 403


@app.errorhandler(500)
def internal_error(error):
    """500 Internal Server Error."""
    app.logger.error(f'Server Error: {error}')
    return render_template('error.html', code=500, message='Internal Server Error'), 500


# Handle unhandled exceptions
@app.errorhandler(Exception)
def handle_exception(error):
    """Catch-all for unhandled exceptions."""
    app.logger.exception(f'Unhandled exception: {error}')
    return render_template('error.html', code=500, message='Something went wrong'), 500


# ============================================================
# 2. LOGGING CONFIGURATION
# ============================================================

def configure_logging(app):
    """Set up logging for the application."""
    
    # Create logs directory
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # --- File Handler (rotating log files) ---
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=1024 * 1024,  # 1 MB per file
        backupCount=10,         # Keep 10 backup files
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    
    # --- Console Handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s: %(message)s'
    ))
    
    # Add handlers to Flask's logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)

configure_logging(app)


# ============================================================
# 3. ROUTES (demonstrating logging & errors)
# ============================================================

@app.route('/')
def index():
    app.logger.info('Homepage accessed')
    return render_template('index.html')


@app.route('/log-demo')
def log_demo():
    """Demonstrate all logging levels."""
    app.logger.debug('This is a DEBUG message')     # Development details
    app.logger.info('This is an INFO message')       # General operations
    app.logger.warning('This is a WARNING message')  # Something unexpected
    app.logger.error('This is an ERROR message')     # Something failed
    app.logger.critical('This is a CRITICAL message') # System is failing
    
    return '''
    <h1>Logging Demo</h1>
    <p>Check the terminal and <code>logs/app.log</code> for messages.</p>
    <a href="/">← Back</a>
    '''


@app.route('/cause-error')
def cause_error():
    """Deliberately cause an error to test error handling."""
    result = 1 / 0  # ZeroDivisionError
    return str(result)


@app.route('/raise-404')
def raise_404():
    """Manually raise a 404."""
    from flask import abort
    abort(404)


# ============================================================
# 4. REQUEST HOOKS FOR LOGGING
# ============================================================

@app.before_request
def log_request():
    """Log every incoming request."""
    app.logger.debug(f'{request.method} {request.path} from {request.remote_addr}')


@app.after_request
def log_response(response):
    """Log every response."""
    app.logger.debug(f'Response: {response.status_code}')
    return response


if __name__ == '__main__':
    app.run(debug=True)
