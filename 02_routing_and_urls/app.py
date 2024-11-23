"""
Module 02 — Routing & URL Building
====================================
Everything about Flask routing: static routes, dynamic routes,
variable rules, URL converters, url_for(), HTTP methods, and
unique URL behavior.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, url_for, request, redirect

app = Flask(__name__)


# ============================================================
# 1. BASIC STATIC ROUTES
# ============================================================

@app.route('/')
def index():
    """Root route — the homepage."""
    # Build a list of all routes for demonstration
    links = [
        '<h1>Module 02 — Routing & URL Building</h1>',
        '<h2>Available Routes:</h2>',
        '<ul>',
        f'<li><a href="{url_for("index")}">/ (Home)</a></li>',
        f'<li><a href="{url_for("about")}">About</a></li>',
        f'<li><a href="{url_for("contact")}">Contact</a></li>',
        f'<li><a href="{url_for("user_profile", username="parth")}">User Profile (parth)</a></li>',
        f'<li><a href="{url_for("show_post", post_id=42)}">Show Post #42</a></li>',
        f'<li><a href="{url_for("show_price", price=19.99)}">Price: $19.99</a></li>',
        f'<li><a href="{url_for("show_path", subpath="docs/api/v2")}">Path Demo</a></li>',
        f'<li><a href="{url_for("show_uuid", uuid_val="550e8400-e29b-41d4-a716-446655440000")}">UUID Demo</a></li>',
        f'<li><a href="{url_for("trailing_slash")}">With Trailing Slash</a></li>',
        f'<li><a href="{url_for("no_trailing_slash")}">Without Trailing Slash</a></li>',
        f'<li><a href="{url_for("login_page")}">Login (GET/POST demo)</a></li>',
        f'<li><a href="{url_for("all_methods_demo")}">All Methods Demo</a></li>',
        '</ul>',
    ]
    return '\n'.join(links)


@app.route('/about')
def about():
    return '<h1>About Page</h1><a href="/">← Back</a>'


@app.route('/contact')
def contact():
    return '<h1>Contact Page</h1><a href="/">← Back</a>'


# ============================================================
# 2. DYNAMIC ROUTES WITH VARIABLE RULES
# ============================================================
# Capture parts of the URL using <variable_name>
# Default converter is 'string' (accepts any text without slashes)

@app.route('/user/<username>')
def user_profile(username):
    """String variable (default converter)."""
    return f'<h1>User: {username}</h1><p>Type: string</p><a href="/">← Back</a>'


# --- URL CONVERTERS ---
# Flask has built-in converters to validate & convert URL variables:
#
# | Converter | Description                          | Example          |
# |-----------|--------------------------------------|------------------|
# | string    | Any text without slashes (default)   | <username>       |
# | int       | Positive integers                    | <int:post_id>    |
# | float     | Positive floating-point values       | <float:price>    |
# | path      | Like string but also accepts slashes | <path:subpath>   |
# | uuid      | UUID strings                         | <uuid:id>        |

@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Integer converter — only matches positive integers."""
    return f'<h1>Post #{post_id}</h1><p>Type: int, Value: {post_id} ({type(post_id).__name__})</p><a href="/">← Back</a>'


@app.route('/price/<float:price>')
def show_price(price):
    """Float converter — matches positive floating-point numbers."""
    return f'<h1>Price: ${price:.2f}</h1><p>Type: float, Value: {price}</p><a href="/">← Back</a>'


@app.route('/path/<path:subpath>')
def show_path(subpath):
    """Path converter — accepts slashes in the URL."""
    return f'<h1>Subpath: {subpath}</h1><p>Type: path (accepts /slashes/)</p><a href="/">← Back</a>'


@app.route('/uuid/<uuid:uuid_val>')
def show_uuid(uuid_val):
    """UUID converter — only matches UUID formatted strings."""
    return f'<h1>UUID: {uuid_val}</h1><p>Type: uuid</p><a href="/">← Back</a>'


# ============================================================
# 3. TRAILING SLASH BEHAVIOR
# ============================================================
# Flask distinguishes between URLs with and without trailing slashes.

@app.route('/projects/')
def trailing_slash():
    """URL with trailing slash — behaves like a folder.
    
    Visiting /projects  → Redirects to /projects/ (301)
    Visiting /projects/ → Works directly
    """
    return '<h1>Trailing Slash Route</h1><p>/projects/ — Flask redirects /projects → /projects/</p><a href="/">← Back</a>'


@app.route('/about-us')
def no_trailing_slash():
    """URL without trailing slash — behaves like a file.
    
    Visiting /about-us  → Works directly
    Visiting /about-us/ → Returns 404!
    """
    return '<h1>No Trailing Slash</h1><p>/about-us — Visiting /about-us/ gives 404!</p><a href="/">← Back</a>'


# ============================================================
# 4. URL BUILDING WITH url_for()
# ============================================================
# url_for() builds URLs for a given function name.
# This is preferred over hardcoding URLs because:
#   - It's reverse lookup: function name → URL
#   - It handles escaping and relative paths
#   - If you change a route URL, all url_for() calls update automatically

@app.route('/url-demo')
def url_demo():
    """Demonstrate url_for() with various arguments."""
    urls = {
        'index': url_for('index'),
        'about': url_for('about'),
        'user_profile (parth)': url_for('user_profile', username='parth'),
        'show_post (id=5)': url_for('show_post', post_id=5),
        'show_price (19.99)': url_for('show_price', price=19.99),
        # Extra keyword arguments become query string parameters
        'index with query params': url_for('index', page=2, sort='name'),
    }
    
    html = '<h1>url_for() Demos</h1><ul>'
    for name, url in urls.items():
        html += f'<li><strong>{name}</strong>: <code>{url}</code> → <a href="{url}">Visit</a></li>'
    html += '</ul><a href="/">← Back</a>'
    return html


# ============================================================
# 5. HTTP METHODS
# ============================================================
# By default, routes only respond to GET requests.
# Use the methods parameter to accept other HTTP methods.

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Handle both GET (show form) and POST (process form)."""
    if request.method == 'POST':
        username = request.form.get('username', 'unknown')
        return f'<h1>Welcome, {username}!</h1><p>POST request processed.</p><a href="/">← Back</a>'
    
    # GET — show the form
    return '''
        <h1>Login (GET/POST Demo)</h1>
        <form method="POST">
            <label>Username: <input type="text" name="username" required></label><br><br>
            <button type="submit">Login (POST)</button>
        </form>
        <br><a href="/">← Back</a>
    '''


@app.route('/api/data', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def all_methods_demo():
    """Respond to all common HTTP methods."""
    method = request.method
    info = {
        'GET': 'Retrieve data (read-only, idempotent)',
        'POST': 'Create new data (not idempotent)',
        'PUT': 'Update/replace data (idempotent)',
        'DELETE': 'Delete data (idempotent)',
        'PATCH': 'Partially update data (not necessarily idempotent)',
    }
    
    return f'''
        <h1>HTTP Method: {method}</h1>
        <p><strong>Purpose:</strong> {info.get(method, "Unknown")}</p>
        <p>Try different methods using curl or Postman:</p>
        <pre>
curl -X GET    http://127.0.0.1:5000/api/data
curl -X POST   http://127.0.0.1:5000/api/data
curl -X PUT    http://127.0.0.1:5000/api/data
curl -X DELETE http://127.0.0.1:5000/api/data
curl -X PATCH  http://127.0.0.1:5000/api/data
        </pre>
        <a href="/">← Back</a>
    '''


# ============================================================
# 6. MULTIPLE ROUTES FOR ONE FUNCTION
# ============================================================
# You can stack multiple decorators on a single view function.

@app.route('/page')
@app.route('/page/<int:num>')
def paginated(num=1):
    """Two routes pointing to the same function with a default."""
    return f'<h1>Page {num}</h1><p>/page defaults to page 1, /page/3 shows page 3</p><a href="/">← Back</a>'


# ============================================================
# 7. REDIRECT
# ============================================================

@app.route('/old-page')
def old_page():
    """Redirect from an old URL to a new one."""
    return redirect(url_for('about'))


# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)
