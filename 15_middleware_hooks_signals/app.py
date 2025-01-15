"""
Module 15 — Middleware, Hooks & Signals
==========================================
Request lifecycle hooks (before/after request, teardown),
WSGI middleware, and Flask signals (blinker).

Run:  pip install blinker
      python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, request, g, jsonify
from time import time
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# ============================================================
# 1. REQUEST LIFECYCLE HOOKS
# ============================================================
# Order: before_request → view function → after_request → teardown_request

@app.before_request
def before_request_handler():
    """Runs BEFORE every request.
    
    Common uses:
    - Authentication checks
    - Request logging
    - Setting up per-request resources
    - Timing requests
    """
    g.start_time = time()
    g.request_id = id(request)  # Simple request identifier
    app.logger.info(f'[{request.method}] {request.path} — START')


@app.after_request
def after_request_handler(response):
    """Runs AFTER every request (if no unhandled exception).
    
    MUST return the response (can modify it).
    Common uses:
    - Adding headers (CORS, security)
    - Logging response info
    - Modifying response
    """
    # Add timing header
    duration = time() - g.get('start_time', time())
    response.headers['X-Request-Duration'] = f'{duration:.4f}s'
    response.headers['X-Request-Id'] = str(g.get('request_id', ''))
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    
    app.logger.info(f'[{request.method}] {request.path} — {response.status_code} ({duration:.4f}s)')
    return response


@app.teardown_request
def teardown_request_handler(exception):
    """Runs at the VERY END, even if there was an exception.
    
    Common uses:
    - Closing database connections
    - Cleaning up resources
    - Logging exceptions
    """
    if exception:
        app.logger.error(f'Request failed: {exception}')


@app.teardown_appcontext
def teardown_appcontext_handler(exception):
    """Runs when the application context ends.
    
    Similar to teardown_request but at app context level.
    Used for cleanup that's per-app-context, not per-request.
    """
    pass  # Database connection cleanup would go here


# ============================================================
# 2. MULTIPLE before_request HANDLERS
# ============================================================
# They run in order of registration. If any returns a response,
# the rest are skipped and the view function is NOT called.

@app.before_request
def check_maintenance():
    """Check if site is in maintenance mode."""
    if app.config.get('MAINTENANCE_MODE'):
        return jsonify({'message': 'Under maintenance'}), 503


# ============================================================
# 3. SIGNALS (requires blinker)
# ============================================================

try:
    from flask import request_started, request_finished, got_request_exception
    from flask import template_rendered, before_render_template
    
    def log_request_started(sender, **kwargs):
        """Signal: fires when a request starts."""
        app.logger.debug(f'Signal: request_started from {sender.name}')
    
    def log_request_finished(sender, response, **kwargs):
        """Signal: fires when a request finishes."""
        app.logger.debug(f'Signal: request_finished — {response.status_code}')
    
    def log_template_rendered(sender, template, context, **kwargs):
        """Signal: fires when a template is rendered."""
        app.logger.debug(f'Signal: template_rendered — {template.name}')
    
    def log_exception(sender, exception, **kwargs):
        """Signal: fires on unhandled exceptions."""
        app.logger.error(f'Signal: got_request_exception — {exception}')
    
    # Connect signals
    request_started.connect(log_request_started, app)
    request_finished.connect(log_request_finished, app)
    template_rendered.connect(log_template_rendered, app)
    got_request_exception.connect(log_exception, app)

except ImportError:
    app.logger.warning('blinker not installed — signals unavailable')


# ============================================================
# 4. CUSTOM SIGNALS
# ============================================================

try:
    from blinker import Namespace
    
    # Create a namespace for app signals
    app_signals = Namespace()
    
    # Define custom signals
    user_logged_in = app_signals.signal('user-logged-in')
    item_created = app_signals.signal('item-created')
    
    # Connect handler
    def on_user_login(sender, user=None, **kwargs):
        app.logger.info(f'Custom signal: {user} logged in')
    
    user_logged_in.connect(on_user_login)
    
except ImportError:
    pass


# ============================================================
# 5. WSGI MIDDLEWARE
# ============================================================

class RequestTimingMiddleware:
    """WSGI Middleware — wraps the entire WSGI application.
    
    Runs before Flask even sees the request.
    Lower level than before_request/after_request.
    """
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        start = time()
        
        def custom_start_response(status, headers, exc_info=None):
            # Add timing header at WSGI level
            duration = time() - start
            headers.append(('X-WSGI-Duration', f'{duration:.4f}s'))
            return start_response(status, headers, exc_info)
        
        return self.app(environ, custom_start_response)


# Apply WSGI middleware
# app.wsgi_app = RequestTimingMiddleware(app.wsgi_app)


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    return '''
    <h1>Module 15 — Middleware, Hooks & Signals</h1>
    <p>Check terminal output for hook/signal logs.</p>
    <ul>
        <li><a href="/demo">Demo endpoint</a></li>
        <li><a href="/headers">See response headers</a></li>
        <li><a href="/lifecycle">Request lifecycle diagram</a></li>
    </ul>
    '''


@app.route('/demo')
def demo():
    return jsonify({'message': 'Check terminal for hook logs!'})


@app.route('/headers')
def show_headers():
    return jsonify({
        'note': 'Check the Response Headers in DevTools',
        'headers_added': ['X-Request-Duration', 'X-Request-Id',
                         'X-Content-Type-Options', 'X-Frame-Options'],
    })


@app.route('/lifecycle')
def lifecycle():
    return '''
    <h1>Request Lifecycle</h1>
    <pre>
    Client Request
        ↓
    WSGI Middleware (if any)
        ↓
    before_request handlers (in order)
        ↓   ← If any returns a response, skip to after_request
    View Function
        ↓
    after_request handlers (reverse order)
        ↓
    teardown_request (always runs)
        ↓
    teardown_appcontext (always runs)
        ↓
    Response sent to client
    </pre>
    <a href="/">← Back</a>
    '''


if __name__ == '__main__':
    app.run(debug=True)
