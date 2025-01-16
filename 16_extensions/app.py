"""
Module 16 — Flask Extensions
==============================
Common Flask extensions: Flask-Mail, Flask-Caching, Flask-Limiter,
Flask-Migrate, Flask-CORS — all with practical examples.

Run:  pip install flask-caching flask-cors flask-limiter
      python app.py
"""

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


# ============================================================
# 1. FLASK-CACHING — Response caching
# ============================================================

from flask_caching import Cache

app.config['CACHE_TYPE'] = 'SimpleCache'       # In-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 300       # 5 minutes

cache = Cache(app)

@app.route('/cached')
@cache.cached(timeout=60)  # Cache this response for 60 seconds
def cached_view():
    """This response is cached for 60 seconds."""
    import datetime
    return jsonify({
        'message': 'This is cached!',
        'generated_at': datetime.datetime.now().isoformat(),
        'note': 'Refresh — timestamp stays the same for 60s'
    })

@app.route('/cached-key/<name>')
@cache.cached(timeout=30, key_prefix='user_%s')
def cached_by_key(name):
    """Cached per unique URL path."""
    return jsonify({'name': name, 'cached': True})

@app.route('/clear-cache')
def clear_cache():
    cache.clear()
    return jsonify({'message': 'Cache cleared!'})


# ============================================================
# 2. FLASK-CORS — Cross-Origin Resource Sharing
# ============================================================

from flask_cors import CORS

# Enable CORS for all routes
CORS(app, resources={
    r'/api/*': {
        'origins': ['http://localhost:3000', 'https://mysite.com'],
        'methods': ['GET', 'POST', 'PUT', 'DELETE'],
        'allow_headers': ['Content-Type', 'Authorization'],
    }
})

@app.route('/api/data')
def api_data():
    """CORS-enabled endpoint."""
    return jsonify({'data': 'accessible from allowed origins'})


# ============================================================
# 3. FLASK-LIMITER — Rate Limiting
# ============================================================

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=['200 per day', '50 per hour'],  # Global limits
    storage_uri='memory://',
)

@app.route('/limited')
@limiter.limit('5 per minute')  # Override: 5 requests per minute
def rate_limited():
    return jsonify({'message': 'You can hit this 5 times per minute'})

@app.route('/unlimited')
@limiter.exempt  # No rate limiting on this route
def unlimited():
    return jsonify({'message': 'No rate limit here!'})


# ============================================================
# 4. INDEX
# ============================================================

@app.route('/')
def index():
    return '''
    <h1>Module 16 — Flask Extensions</h1>
    <h2>Flask-Caching</h2>
    <ul>
        <li><a href="/cached">Cached Response (60s)</a></li>
        <li><a href="/cached-key/parth">Cached by Key</a></li>
        <li><a href="/clear-cache">Clear Cache</a></li>
    </ul>
    <h2>Flask-CORS</h2>
    <ul><li><a href="/api/data">CORS-enabled API</a></li></ul>
    <h2>Flask-Limiter</h2>
    <ul>
        <li><a href="/limited">Rate Limited (5/min)</a></li>
        <li><a href="/unlimited">Unlimited</a></li>
    </ul>
    '''


if __name__ == '__main__':
    app.run(debug=True)
