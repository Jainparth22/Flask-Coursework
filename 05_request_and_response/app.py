"""
Module 05 — Request & Response
================================
The request object, response building, cookies, redirects,
error handling (abort), JSON responses, and custom responses.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

from flask import (
    Flask, request, make_response, jsonify,
    redirect, url_for, abort
)
import json

app = Flask(__name__)


# ============================================================
# HOMEPAGE — Navigation
# ============================================================

@app.route('/')
def index():
    return '''
    <h1>Module 05 — Request & Response</h1>
    <h2>Request Object Demos</h2>
    <ul>
        <li><a href="/request-info">Request Info (headers, method, URL)</a></li>
        <li><a href="/query?name=Parth&age=25&lang=python&lang=flask">Query Parameters</a></li>
        <li><a href="/form-demo">Form Data (POST)</a></li>
        <li><a href="/json-echo">JSON Echo (use curl/Postman)</a></li>
    </ul>
    <h2>Response Demos</h2>
    <ul>
        <li><a href="/string-response">String Response</a></li>
        <li><a href="/tuple-response">Tuple Response (body, status, headers)</a></li>
        <li><a href="/custom-response">Custom Response with make_response()</a></li>
        <li><a href="/json-response">JSON Response with jsonify()</a></li>
        <li><a href="/json-response-v2">JSON Response (dict shorthand)</a></li>
    </ul>
    <h2>Cookies</h2>
    <ul>
        <li><a href="/set-cookie">Set a Cookie</a></li>
        <li><a href="/get-cookie">Read the Cookie</a></li>
        <li><a href="/delete-cookie">Delete the Cookie</a></li>
    </ul>
    <h2>Redirects & Errors</h2>
    <ul>
        <li><a href="/redirect-demo">Redirect to Homepage</a></li>
        <li><a href="/abort-404">Trigger 404</a></li>
        <li><a href="/abort-403">Trigger 403 Forbidden</a></li>
        <li><a href="/abort-500">Trigger 500 Server Error</a></li>
    </ul>
    '''


# ============================================================
# 1. THE REQUEST OBJECT
# ============================================================
# Flask's `request` is a proxy to the current HTTP request.
# It's available in any view function without importing per-request.

@app.route('/request-info')
def request_info():
    """Show all major request object attributes."""
    info = {
        'request.method': request.method,
        'request.url': request.url,
        'request.base_url': request.base_url,
        'request.host_url': request.host_url,
        'request.host': request.host,
        'request.path': request.path,
        'request.full_path': request.full_path,
        'request.scheme': request.scheme,
        'request.remote_addr': request.remote_addr,
        'request.content_type': request.content_type,
        'request.user_agent': str(request.user_agent),
        'request.referrer': request.referrer,
        'request.is_json': request.is_json,
        'request.headers (sample)': dict(list(request.headers)[:5]),
    }
    return jsonify(info)


# ============================================================
# 2. QUERY PARAMETERS — request.args
# ============================================================

@app.route('/query')
def query_params():
    """Read query string parameters from the URL.
    
    Try: /query?name=Parth&age=25&lang=python&lang=flask
    """
    # request.args is an ImmutableMultiDict
    name = request.args.get('name', 'Guest')          # Single value with default
    age = request.args.get('age', 0, type=int)         # With type conversion
    langs = request.args.getlist('lang')               # Multiple values for same key
    all_params = request.args.to_dict(flat=False)      # All params as dict
    
    return jsonify({
        'name (get)': name,
        'age (get with type=int)': age,
        'lang (getlist)': langs,
        'all_params (to_dict)': all_params,
        'raw_query_string': request.query_string.decode(),
    })


# ============================================================
# 3. FORM DATA — request.form
# ============================================================

@app.route('/form-demo', methods=['GET', 'POST'])
def form_demo():
    """Handle form submissions via POST."""
    if request.method == 'POST':
        # request.form is an ImmutableMultiDict for POST form data
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        # request.form['key'] raises KeyError if missing
        # request.form.get('key') returns None if missing
        return jsonify({
            'received': {
                'username': username,
                'email': email,
            },
            'all_form_data': request.form.to_dict(),
        })
    
    return '''
    <h1>Form Data Demo</h1>
    <form method="POST">
        <label>Username: <input type="text" name="username" value="parth"></label><br><br>
        <label>Email: <input type="email" name="email" value="parth@example.com"></label><br><br>
        <button type="submit">Submit (POST)</button>
    </form>
    <p><a href="/">← Back</a></p>
    '''


# ============================================================
# 4. JSON DATA — request.json / request.get_json()
# ============================================================

@app.route('/json-echo', methods=['GET', 'POST'])
def json_echo():
    """Echo back JSON data sent in the request body.
    
    Test with curl:
        curl -X POST http://127.0.0.1:5000/json-echo \
             -H "Content-Type: application/json" \
             -d '{"name": "Parth", "age": 25}'
    """
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 415
        
        # request.json — shortcut for request.get_json()
        # request.get_json(force=True) — parse even without Content-Type header
        # request.get_json(silent=True) — return None instead of 400 on parse failure
        data = request.get_json()
        
        return jsonify({
            'you_sent': data,
            'is_json': request.is_json,
            'content_type': request.content_type,
        })
    
    return jsonify({
        'message': 'Send a POST request with JSON body',
        'example': 'curl -X POST -H "Content-Type: application/json" -d \'{"key":"value"}\' http://127.0.0.1:5000/json-echo'
    })


# ============================================================
# 5. FILE UPLOADS — request.files
# ============================================================

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file uploads via multipart form."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400
        
        f = request.files['file']
        if f.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # In production, use werkzeug.utils.secure_filename()
        # and save to a secure location
        return jsonify({
            'filename': f.filename,
            'content_type': f.content_type,
            'size_note': 'File received but not saved (demo only)',
        })
    
    return '''
    <h1>File Upload</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file"><br><br>
        <button type="submit">Upload</button>
    </form>
    <p><a href="/">← Back</a></p>
    '''


# ============================================================
# 6. RESPONSES — Different Ways to Return Data
# ============================================================

@app.route('/string-response')
def string_response():
    """Returning a string — Flask wraps it in a Response with status 200."""
    return '<h1>Simple String Response</h1><p>Status: 200, Content-Type: text/html</p><a href="/">← Back</a>'


@app.route('/tuple-response')
def tuple_response():
    """Return a tuple: (body, status_code, headers).
    
    You can return:
      - (body, status)
      - (body, headers)
      - (body, status, headers)
    """
    return (
        '<h1>Tuple Response</h1><p>Status: 201 Created</p><a href="/">← Back</a>',
        201,
        {'X-Custom-Header': 'Hello from Flask!'}
    )


@app.route('/custom-response')
def custom_response():
    """Use make_response() for full response control."""
    resp = make_response('<h1>Custom Response</h1><p>Check the response headers!</p><a href="/">← Back</a>')
    resp.status_code = 200
    resp.headers['X-Powered-By'] = 'Flask Coursework'
    resp.headers['X-Module'] = '05'
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp


@app.route('/json-response')
def json_response():
    """Use jsonify() — sets Content-Type to application/json."""
    return jsonify({
        'message': 'Hello from JSON!',
        'module': 5,
        'topics': ['request', 'response', 'cookies', 'redirects'],
    })


@app.route('/json-response-v2')
def json_response_v2():
    """Return a dict directly — Flask auto-converts to JSON (Flask 1.0+)."""
    return {
        'message': 'Dict returned directly!',
        'note': 'Flask automatically calls jsonify() on dicts',
    }


# ============================================================
# 7. COOKIES
# ============================================================

@app.route('/set-cookie')
def set_cookie():
    """Set a cookie on the response."""
    resp = make_response('<h1>Cookie Set! 🍪</h1><p><a href="/get-cookie">Read it</a></p><a href="/">← Back</a>')
    resp.set_cookie(
        'username',           # Cookie name
        'parth',              # Cookie value
        max_age=3600,         # Expires in 1 hour (seconds)
        httponly=True,        # Not accessible via JavaScript
        # secure=True,        # Only sent over HTTPS (enable in production)
        samesite='Lax',       # CSRF protection: 'Strict', 'Lax', or 'None'
    )
    return resp


@app.route('/get-cookie')
def get_cookie():
    """Read a cookie from the request."""
    username = request.cookies.get('username', 'Not set')
    return f'<h1>Cookie Value: {username}</h1><a href="/">← Back</a>'


@app.route('/delete-cookie')
def delete_cookie():
    """Delete a cookie by setting max_age=0."""
    resp = make_response('<h1>Cookie Deleted! ❌</h1><a href="/">← Back</a>')
    resp.delete_cookie('username')  # Shorthand for set_cookie with max_age=0
    return resp


# ============================================================
# 8. REDIRECTS
# ============================================================

@app.route('/redirect-demo')
def redirect_demo():
    """Redirect to another URL."""
    # redirect() returns a 302 response by default
    # Use code=301 for permanent redirects
    return redirect(url_for('index'))


@app.route('/redirect-external')
def redirect_external():
    """Redirect to an external URL."""
    return redirect('https://flask.palletsprojects.com')


# ============================================================
# 9. ERROR RESPONSES WITH abort()
# ============================================================

@app.route('/abort-404')
def trigger_404():
    """Trigger a 404 Not Found error."""
    abort(404)  # Raises an HTTPException


@app.route('/abort-403')
def trigger_403():
    """Trigger a 403 Forbidden error."""
    abort(403)


@app.route('/abort-500')
def trigger_500():
    """Trigger a 500 Internal Server Error."""
    abort(500)


# Custom error handlers (override default error pages)
@app.errorhandler(404)
def not_found(error):
    return '<h1>404 — Page Not Found</h1><p>The requested URL was not found.</p><a href="/">← Home</a>', 404


@app.errorhandler(403)
def forbidden(error):
    return '<h1>403 — Forbidden</h1><p>You don\'t have permission to access this.</p><a href="/">← Home</a>', 403


@app.errorhandler(500)
def server_error(error):
    return '<h1>500 — Internal Server Error</h1><p>Something went wrong on our end.</p><a href="/">← Home</a>', 500


# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)
