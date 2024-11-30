# Flask Complete Theory

A deep dive into Flask's philosophy, internals, and core mechanics — the **why** behind the **how**.

---

## A. What is Flask?

### Microframework Philosophy

Flask is a **micro web framework** for Python, created by **Armin Ronacher** in 2010. The "micro" does NOT mean:
- ❌ Limited functionality
- ❌ Only for small apps
- ❌ Missing features

It MEANS:
- ✅ **Minimal core** — doesn't force decisions on you
- ✅ **No bundled ORM, form library, or admin panel** (unlike Django)
- ✅ **You choose** your tools (SQLAlchemy, WTForms, etc.)
- ✅ **Extensible** — rich ecosystem of extensions

> "Flask aims to keep the core simple but extensible." — Flask Docs

### Flask's Two Pillars

Flask is built on top of two libraries by the same team (Pallets):

| Library | Role | What It Does |
|---------|------|-------------|
| **Werkzeug** | WSGI toolkit | HTTP request/response handling, URL routing, debugging |
| **Jinja2** | Template engine | HTML rendering with variables, loops, inheritance |

```
Flask = Werkzeug (HTTP/WSGI) + Jinja2 (Templates) + Glue Code
```

### When to Use Flask

| Use Flask When | Use Django When |
|---------------|----------------|
| Building APIs | Need admin panel out of the box |
| Microservices | Building content-heavy sites |
| You want control over architecture | Want batteries-included |
| Learning web development | Need built-in ORM, auth, admin |
| Prototyping quickly | Large team with conventions |

### Flask vs FastAPI vs Django

| Feature | Flask | FastAPI | Django |
|---------|-------|---------|--------|
| Type | Micro | Micro/Modern | Full-stack |
| Async | Limited (2.0+) | Native | Limited (4.0+) |
| Auto docs | ❌ (extension) | ✅ Swagger built-in | ❌ |
| ORM | ❌ (extension) | ❌ (extension) | ✅ Built-in |
| Validation | ❌ (Marshmallow) | ✅ Pydantic | ✅ Forms |
| Learning curve | Low | Low | Medium |
| Maturity | 2010+ (very mature) | 2018+ | 2005+ (most mature) |

---

## B. WSGI vs ASGI

### What is WSGI?

**WSGI** (Web Server Gateway Interface) is the Python standard for how web servers communicate with web applications. Defined in **PEP 3333**.

```
Browser → Web Server (Nginx) → WSGI Server (Gunicorn) → Flask App
```

### Flask as a WSGI Application

Every Flask app IS a WSGI application:

```python
app = Flask(__name__)

# Flask's __call__ method makes it a WSGI app:
# app(environ, start_response)  ← This is the WSGI interface
```

Under the hood:

```python
# Simplified WSGI interface
def application(environ, start_response):
    # environ = dict with HTTP request info (METHOD, PATH, HEADERS...)
    # start_response = callback to set status and headers
    status = '200 OK'
    headers = [('Content-Type', 'text/html')]
    start_response(status, headers)
    return [b'Hello World']
```

Flask wraps this complexity:
```python
@app.route('/')
def hello():
    return 'Hello World'  # Flask converts this to a proper WSGI response
```

### What is ASGI?

**ASGI** (Asynchronous Server Gateway Interface) extends WSGI to support:
- `async`/`await`
- WebSockets
- Long-lived connections
- HTTP/2

### WSGI vs ASGI Comparison

| Feature | WSGI (Flask) | ASGI (FastAPI, Quart) |
|---------|-------------|----------------------|
| Sync support | ✅ Native | ✅ Yes |
| Async support | ⚠️ Limited (Flask 2.0+) | ✅ Native |
| WebSockets | ❌ (needs Flask-SocketIO) | ✅ Native |
| Protocol | HTTP/1.1 | HTTP/1.1, HTTP/2, WebSocket |
| Servers | Gunicorn, uWSGI, Waitress | Uvicorn, Hypercorn, Daphne |
| Performance | Good | Better for I/O-bound |

### Flask's Async Limitations

Flask 2.0+ supports `async def` views, BUT:
```python
@app.route('/async')
async def async_view():
    # This works, but Flask runs it in a THREAD (not true async event loop)
    await asyncio.sleep(1)
    return 'Done'
```

For **true async**, consider:
- **Quart** — Flask-compatible ASGI framework (same API)
- **FastAPI** — Built for async from the ground up

### Request Lifecycle in Flask

```
1. Client sends HTTP request
        ↓
2. WSGI server (Gunicorn) receives it
        ↓
3. WSGI server calls Flask app (environ, start_response)
        ↓
4. Flask creates Request object from environ
        ↓
5. Flask pushes Application Context
        ↓
6. Flask pushes Request Context
        ↓
7. before_request hooks run
        ↓  (if any returns a response, skip to step 10)
8. URL routing → matches route → calls view function
        ↓
9. View function returns response
        ↓
10. after_request hooks run (can modify response)
        ↓
11. Flask pops Request Context
        ↓
12. teardown_request runs (cleanup, always runs)
        ↓
13. Flask pops Application Context
        ↓
14. teardown_appcontext runs
        ↓
15. WSGI server sends HTTP response to client
```

---

## C. Core Flask Internals

### Werkzeug — The WSGI Toolkit

Werkzeug provides everything Flask needs for HTTP:

```python
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
```

| Werkzeug Component | Flask Uses It For |
|-------------------|-------------------|
| `Request` | `flask.request` (wraps it) |
| `Response` | Flask response objects |
| `Map` + `Rule` | URL routing (`@app.route()`) |
| `run_simple` | Development server |
| `generate_password_hash` | Password security |
| `secure_filename` | Safe file uploads |
| `DebuggedApplication` | Debug mode with traceback |

### Jinja2 — The Template Engine

```
{{ variable }}          → Output a variable
{% if condition %}      → Logic (if, for, block)
{# comment #}           → Comments (not rendered)
{{ var | filter }}       → Apply filters
{% macro name() %}      → Reusable template functions
{% extends "base" %}    → Template inheritance
{% include "partial" %} → Include another template
```

Jinja2 provides:
- **Auto-escaping** — prevents XSS by default
- **Sandboxed execution** — templates can't access dangerous Python
- **Template inheritance** — DRY layouts with `{% block %}`

### Application Context

The **application context** tracks app-level data during a request or CLI command.

```python
from flask import current_app, g

# current_app → proxy to the active Flask app
# g           → per-request temporary storage (dies after request)
```

Why contexts exist:
```python
# Flask allows MULTIPLE apps in one process
app1 = Flask('app1')
app2 = Flask('app2')

# current_app dynamically resolves to whichever app is handling the request
with app1.app_context():
    print(current_app.name)  # 'app1'
```

### Request Context

The **request context** tracks request-level data.

```python
from flask import request, session

# request → current HTTP request data
# session → user session data (signed cookie)
```

Context lifecycle:
```python
# Flask automatically pushes/pops contexts
@app.route('/')
def index():
    # request context is active here
    return request.method  # 'GET'

# Outside a request, there's no context
request.method  # RuntimeError: Working outside of request context
```

Manual context (for testing or CLI):
```python
with app.test_request_context('/hello?name=World'):
    print(request.path)        # /hello
    print(request.args['name']) # World
```

### The Four Context Proxies

| Proxy | Context | Purpose | Lifetime |
|-------|---------|---------|----------|
| `current_app` | App | Reference to the Flask app | App context |
| `g` | App | Per-request temporary storage | Request |
| `request` | Request | Current HTTP request data | Request |
| `session` | Request | User session (signed cookie) | Across requests |

### The `g` Object

```python
from flask import g

@app.before_request
def load_user():
    g.user = get_user_from_session()    # Set
    g.start_time = time.time()          # Set

@app.route('/')
def index():
    return f'Hello {g.user}'            # Read

@app.after_request
def log_time(response):
    duration = time.time() - g.start_time  # Read
    return response

# g is reset for EVERY request — not shared between requests
```

### `__name__` in `Flask(__name__)`

```python
app = Flask(__name__)
```

`__name__` tells Flask where the application is located so it can find:
- `templates/` folder
- `static/` folder
- `instance/` folder

When `__name__` is `'__main__'` (running directly), Flask looks relative to the script.
When it's a package name (e.g., `'myapp'`), Flask looks relative to the package.

---

## D. Installation & Environment

### Python Version Requirements

| Flask Version | Minimum Python |
|--------------|---------------|
| Flask 3.1.x | Python 3.9+ |
| Flask 3.0.x | Python 3.8+ |
| Flask 2.x | Python 3.7+ |
| Flask 1.x | Python 2.7 / 3.4+ |

### Virtual Environments

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install Flask
pip install flask

# Freeze dependencies
pip freeze > requirements.txt
```

### Running the Development Server

```bash
# Method 1: flask run
set FLASK_APP=app.py        # Windows
export FLASK_APP=app.py     # Linux/Mac
flask run

# Method 2: python app.py (with app.run())
python app.py

# Debug mode
flask run --debug
# or
app.run(debug=True)
```

### Debug Mode

Debug mode enables:
1. **Auto-reloader** — restarts server on code changes
2. **Interactive debugger** — in-browser Python debugger on errors
3. **Detailed error pages** — full traceback with code context

> ⚠️ **NEVER** enable debug mode in production — it allows arbitrary code execution!

---

## E. Data Validation with Marshmallow

Flask has no built-in validation like FastAPI's Pydantic. Use **Marshmallow** for API data validation.

### Basic Schema

```python
from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    id = fields.Int(dump_only=True)               # Output only
    name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True)
    age = fields.Int(validate=validate.Range(min=0, max=150))
    role = fields.Str(validate=validate.OneOf(['admin', 'user']))
    created_at = fields.DateTime(dump_only=True)
```

### Usage in Flask

```python
user_schema = UserSchema()

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.get_json())  # Validate + deserialize
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # data is now validated and clean
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user))  # Serialize
```

### Nested Schemas

```python
class AddressSchema(Schema):
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    zip_code = fields.Str()

class UserSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Nested(AddressSchema)                    # Single object
    friends = fields.List(fields.Nested(lambda: UserSchema))  # List of users
```

### Custom Validators

```python
from marshmallow import validates, validates_schema

class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    confirm_password = fields.Str(required=True, load_only=True)
    
    @validates('username')
    def validate_username(self, value):
        if User.query.filter_by(username=value).first():
            raise ValidationError('Username already exists')
    
    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data['password'] != data['confirm_password']:
            raise ValidationError('Passwords must match', field_name='confirm_password')
```

### Marshmallow vs WTForms vs Pydantic

| Feature | Marshmallow | WTForms | Pydantic (FastAPI) |
|---------|------------|---------|-------------------|
| Best for | API validation | HTML forms | API + type hints |
| Serialization | ✅ Yes | ❌ No | ✅ Yes |
| CSRF | ❌ No | ✅ Yes | ❌ No |
| Nested objects | ✅ Yes | Limited | ✅ Yes |
| Flask integration | Manual | Flask-WTF | Not Flask-native |

---

## F. JWT Authentication

### What is JWT?

**JSON Web Token** — a self-contained, encoded token for stateless authentication.

```
Header.Payload.Signature
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.signature
```

### Flask-JWT-Extended

```bash
pip install flask-jwt-extended
```

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'        # Change in production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

# --- Login → get tokens ---
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Bad credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)

# --- Protected route ---
@app.route('/protected')
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(user_id=current_user_id)

# --- Refresh token ---
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_token = create_access_token(identity=identity)
    return jsonify(access_token=new_token)
```

### Session-Based (Flask-Login) vs JWT

| Feature | Session (Flask-Login) | JWT |
|---------|----------------------|-----|
| Storage | Server-side (cookie) | Client-side (token) |
| Stateful | ✅ Yes | ❌ Stateless |
| Best for | Web apps (browser) | APIs, mobile apps |
| Logout | Destroy session | Blacklist token / expire |
| Scalability | Needs session store | ✅ No session store |
| CSRF risk | ✅ Yes (need protection) | ❌ No (not in cookies) |

---

## G. OAuth2 (Third-Party Login)

```bash
pip install authlib
```

```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/callback/google')
def google_callback():
    token = google.authorize_access_token()
    user_info = token['userinfo']
    # user_info contains: email, name, picture, etc.
    # Create or find user in your database
    return jsonify(user_info)
```

---

## H. Password Hashing Algorithms

```python
# 1. Werkzeug (Flask default) — uses scrypt
from werkzeug.security import generate_password_hash, check_password_hash
hash = generate_password_hash('password')        # scrypt by default
check_password_hash(hash, 'password')            # True

# 2. Bcrypt
# pip install bcrypt flask-bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
hash = bcrypt.generate_password_hash('password').decode('utf-8')
bcrypt.check_password_hash(hash, 'password')     # True

# 3. Argon2 (winner of Password Hashing Competition)
# pip install argon2-cffi
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash('password')
ph.verify(hash, 'password')                      # True
```

| Algorithm | Speed | Security | Recommendation |
|-----------|-------|----------|---------------|
| scrypt (Werkzeug) | Slow ✅ | ✅ High | Good default |
| bcrypt | Slow ✅ | ✅ High | Industry standard |
| Argon2 | Configurable | ✅ Highest | Best choice (PHC winner) |
| SHA-256 | Fast ❌ | ❌ Weak | **Never for passwords** |
| MD5 | Fast ❌ | ❌ Broken | **Never use** |

---

## I. Security Best Practices

### CSRF Protection

```python
# Flask-WTF handles this
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# In templates:
<form method="POST">
    {{ form.hidden_tag() }}  <!-- Includes CSRF token -->
</form>

# For AJAX:
<meta name="csrf-token" content="{{ csrf_token() }}">
# Send in header: X-CSRFToken
```

### XSS Prevention

```python
# Jinja2 auto-escapes by default
{{ user_input }}            # ← Auto-escaped (safe)
{{ user_input | safe }}     # ← NOT escaped (dangerous!)

# Never use |safe with user input
# Use Markup() for trusted HTML in Python code
from markupsafe import Markup
```

### Secure Headers

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Or use Flask-Talisman
# pip install flask-talisman
from flask_talisman import Talisman
Talisman(app)  # Adds all security headers + forces HTTPS
```

### Rate Limiting (covered in Module 16)

```python
from flask_limiter import Limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["200/day"])

@app.route('/login', methods=['POST'])
@limiter.limit('5/minute')     # Prevent brute force
def login(): ...
```

### HTTPS Enforcement

```python
# In production config
SESSION_COOKIE_SECURE = True       # Cookie only sent over HTTPS
SESSION_COOKIE_HTTPONLY = True      # Not accessible via JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'    # CSRF protection
PREFERRED_URL_SCHEME = 'https'

# Force HTTPS redirect
from flask_talisman import Talisman
Talisman(app, force_https=True)
```

### Security Checklist

- [ ] `SECRET_KEY` is random and from environment variable
- [ ] Debug mode disabled in production
- [ ] CSRF protection enabled (Flask-WTF)
- [ ] Passwords hashed (never plain text)
- [ ] SQL injection prevented (use ORM/parameterized queries)
- [ ] XSS prevented (Jinja2 auto-escaping, no `|safe` with user input)
- [ ] Secure cookie settings (HTTPOnly, Secure, SameSite)
- [ ] Rate limiting on auth endpoints
- [ ] File upload validation (type, size, `secure_filename`)
- [ ] HTTPS enforced in production
- [ ] Security headers set (X-Frame-Options, CSP, HSTS)
- [ ] Dependencies kept updated

---

## J. Database — Advanced Topics

### Multiple Database Support

```python
# SQLAlchemy supports all major databases
# Just change the URI:

# SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

# PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost:5432/mydb'
# pip install psycopg2-binary

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@localhost:3306/mydb'
# pip install pymysql
```

### Flask-Migrate (Alembic)

```bash
pip install flask-migrate
```

```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```

```bash
flask db init                    # Create migrations/ folder (once)
flask db migrate -m "Add users"  # Generate migration from model changes
flask db upgrade                 # Apply pending migrations
flask db downgrade               # Revert last migration
flask db history                 # Show migration log
flask db current                 # Show current revision
```

### Repository Pattern

Decouple database access from business logic:

```python
# repositories/user_repository.py
class UserRepository:
    def __init__(self, db):
        self.db = db
    
    def get_by_id(self, user_id):
        return User.query.get(user_id)
    
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def create(self, username, email, password_hash):
        user = User(username=username, email=email, password_hash=password_hash)
        self.db.session.add(user)
        self.db.session.commit()
        return user
    
    def delete(self, user):
        self.db.session.delete(user)
        self.db.session.commit()

# services/user_service.py
class UserService:
    def __init__(self, user_repo):
        self.repo = user_repo
    
    def register(self, username, email, password):
        if self.repo.get_by_email(email):
            raise ValueError('Email already registered')
        hash = generate_password_hash(password)
        return self.repo.create(username, email, hash)
```

---

## K. Clean Architecture

### Intermediate Project Structure

```
project/
├── app/
│   ├── __init__.py          ← create_app()
│   ├── extensions.py        ← db, login_manager, cache
│   ├── models/
│   │   ├── user.py
│   │   └── post.py
│   ├── routes/
│   │   ├── auth.py          ← Blueprints
│   │   └── api.py
│   ├── services/
│   │   ├── auth_service.py  ← Business logic
│   │   └── post_service.py
│   ├── repositories/
│   │   └── user_repo.py     ← Data access
│   └── templates/
├── config.py
├── run.py
└── tests/
```

### Professional Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── domain/              ← Business entities (pure Python, no Flask)
│   │   ├── user.py
│   │   └── post.py
│   ├── infrastructure/      ← External services
│   │   ├── database.py
│   │   ├── cache.py
│   │   └── email.py
│   ├── services/            ← Business logic
│   │   ├── auth_service.py
│   │   └── post_service.py
│   ├── api/                 ← HTTP layer (blueprints, serialization)
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   └── posts.py
│   │   └── schemas.py       ← Marshmallow schemas
│   ├── config/
│   │   ├── settings.py
│   │   └── logging.py
│   └── extensions.py
├── migrations/
├── tests/
├── docker-compose.yml
└── Dockerfile
```

### Services Layer Pattern

```python
# services/post_service.py
class PostService:
    def __init__(self, db):
        self.db = db
    
    def create_post(self, title, body, author_id):
        """Business logic lives here, NOT in routes."""
        if len(title) < 3:
            raise ValueError('Title too short')
        post = Post(title=title, body=body, user_id=author_id)
        self.db.session.add(post)
        self.db.session.commit()
        return post

# routes/posts.py — thin controller
@posts_bp.route('/new', methods=['POST'])
@login_required
def new_post():
    try:
        post = post_service.create_post(
            request.form['title'],
            request.form['body'],
            current_user.id
        )
        flash('Published!')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('main.index'))
```

---

## L. WebSockets (Flask-SocketIO)

```bash
pip install flask-socketio
```

```python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

# --- Events ---
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    print(f'Message: {data}')
    emit('response', {'data': f'Echo: {data}'})      # Send to sender
    emit('broadcast', {'data': data}, broadcast=True)  # Send to ALL

# --- Rooms ---
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'Joined {room}'}, to=room)

# --- Run ---
if __name__ == '__main__':
    socketio.run(app, debug=True)  # NOT app.run()!
```

Client:
```html
<script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
<script>
    const socket = io();
    socket.on('response', data => console.log(data));
    socket.emit('message', 'Hello!');
</script>
```

---

## M. WebHooks

Receiving events from external services (GitHub, Stripe, etc.):

```python
import hmac, hashlib

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    # 1. Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    secret = b'your-webhook-secret'
    expected = 'sha256=' + hmac.new(secret, request.data, hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(signature, expected):
        return 'Invalid signature', 403
    
    # 2. Process event
    event = request.headers.get('X-GitHub-Event')
    payload = request.get_json()
    
    if event == 'push':
        branch = payload['ref']
        commits = payload['commits']
        print(f'Push to {branch}: {len(commits)} commits')
    
    return 'OK', 200
```

Key practices:
- Always **verify signatures** (HMAC)
- Use `hmac.compare_digest()` (timing-safe comparison)
- Return `200` quickly, process async if heavy
- Log all incoming webhooks
- Use a secret shared with the sender

---

## N. Docker Compose

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=change-me
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  celery:
    build: .
    command: celery -A app.celery worker --loglevel=info
    depends_on:
      - redis

volumes:
  postgres_data:
```

```bash
docker-compose up -d          # Start all services
docker-compose down           # Stop all
docker-compose logs -f web    # Follow logs
docker-compose exec web bash  # Shell into container
```

---

## O. CI/CD (GitHub Actions)

```yaml
# .github/workflows/flask.yml
name: Flask CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest --tb=short -v
      
      - name: Lint
        run: |
          pip install flake8
          flake8 app/ --max-line-length 120

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: echo "Deploy to production here"
```

---

## P. Scalability Concepts

### Stateless Design

```python
# ❌ BAD — storing state in app memory
users_cache = {}  # Lost on restart, different per worker

# ✅ GOOD — external state store
# Use Redis for cache, PostgreSQL for data
cache.set('user:1', user_data)     # Redis
db.session.add(user)               # Database
```

### Horizontal Scaling

```
                    ┌─── Flask Worker 1
Client → Nginx ─── ├─── Flask Worker 2
(Load Balancer)     ├─── Flask Worker 3
                    └─── Flask Worker 4
                              ↕
                    ┌─── PostgreSQL
                    └─── Redis (sessions + cache)
```

### Key Principles

| Principle | How |
|-----------|-----|
| **Stateless app** | No in-memory state; use Redis/DB |
| **External sessions** | Store sessions in Redis, not files |
| **Database connection pooling** | SQLAlchemy pool_size, max_overflow |
| **Caching** | Redis/Memcached for frequent queries |
| **Async tasks** | Celery for background work |
| **CDN** | Serve static files from CDN, not Flask |
| **Database read replicas** | Split read/write workloads |
| **Containerization** | Docker for consistent environments |
| **Health checks** | `/health` endpoint for load balancers |

### Streaming Responses

```python
from flask import Response, stream_with_context

@app.route('/stream')
def stream():
    def generate():
        for i in range(100):
            yield f'data: Line {i}\n\n'
            time.sleep(0.1)
    
    return Response(
        stream_with_context(generate()),
        content_type='text/event-stream'
    )
```

---

## Q. Coverage Mapping

Where each topic lives in this coursework:

| Topic | Theory | Code Module |
|-------|--------|-------------|
| What is Flask / Microframework | This file (§A) | M01 |
| WSGI vs ASGI | This file (§B) | — |
| Flask Internals / Contexts | This file (§C) | — |
| Installation & Setup | This file (§D) | M01 |
| Routing | M02 DOCS | M02 |
| HTTP Methods | M02 DOCS, M12 DOCS | M02, M12 |
| Request Handling | M05 DOCS | M05 |
| Response Handling | M05 DOCS | M05 |
| Templates (Jinja2) | M03 DOCS | M03 |
| Static Files | M04 DOCS | M04 |
| Forms / WTForms | M06 DOCS | M06 |
| Cookies / Sessions / Flashing | M07 DOCS | M07 |
| Database (SQLite + SQLAlchemy) | M08 DOCS | M08 |
| Blueprints / Factory | M09 DOCS | M09 |
| Configuration | M10 DOCS | M10 |
| Authentication (Flask-Login) | M11 DOCS | M11 |
| REST APIs | M12 DOCS | M12 |
| Swagger / OpenAPI | SWAGGER.md | — |
| Error Handling / Logging | M13 DOCS | M13 |
| Testing (pytest) | M14 DOCS | M14 |
| Middleware / Hooks / Signals | M15 DOCS | M15 |
| Extensions (Cache/CORS/Limiter) | M16 DOCS | M16 |
| Class-Based Views | M17 DOCS | M17 |
| Async / Background / Celery | M18 DOCS | M18 |
| Deployment (Gunicorn/Docker/Nginx) | M19 DOCS | M19 |
| Capstone Blog | M20 DOCS | M20 |
| Marshmallow (validation) | This file (§E) | — |
| JWT Authentication | This file (§F) | — |
| OAuth2 | This file (§G) | — |
| Password Hashing | This file (§H) | M11 |
| Security Best Practices | This file (§I) | — |
| Migrations (Flask-Migrate) | This file (§J) | — |
| Repository / Services Pattern | This file (§K) | — |
| WebSockets | This file (§L) | — |
| WebHooks | This file (§M) | — |
| Docker Compose | This file (§N) | — |
| CI/CD | This file (§O) | — |
| Scalability | This file (§P) | — |
| ML with Flask | ML_WITH_FLASK.md | — |
| File Uploads | M06 DOCS | M06 |
| CORS | M16 DOCS | M16 |
| Rate Limiting | M16 DOCS | M16 |
| Streaming Responses | This file (§P) | — |
| Flask CLI Commands | This file (§R) | M08 (init-db) |
| Context Processors | This file (§S) | — |
| File Downloads / send_file | This file (§T) | — |
| Flask Shell | This file (§U) | — |
| ProxyFix Middleware | This file (§V) | — |
| Flask-Admin | This file (§W) | — |
| i18n (Flask-Babel) | This file (§W) | — |
| HTMX + Flask | This file (§W) | — |
| Sentry (Error Monitoring) | This file (§W) | — |
| Flask-DebugToolbar | This file (§W) | — |

---

## R. Flask CLI Commands

Custom commands via `@app.cli.command()` — for DB seeding, admin tasks, cron jobs.

```python
import click

@app.cli.command('seed')
@click.argument('count', default=10)
def seed_db(count):
    """Seed database with fake data."""
    for i in range(count):
        db.session.add(User(username=f'user{i}', email=f'user{i}@test.com'))
    db.session.commit()
    click.echo(f'Seeded {count} users.')

@app.cli.command('init-db')
def init_db():
    """Create all tables."""
    db.create_all()
    click.echo('Database initialized.')
```

```bash
flask seed 20          # Create 20 users
flask init-db          # Create tables
flask routes           # Show all registered routes (built-in)
```

### CLI with Blueprints

```python
user_cli = AppGroup('user')

@user_cli.command('create')
@click.argument('name')
def create_user(name):
    click.echo(f'Created {name}')

app.cli.add_command(user_cli)
# Usage: flask user create parth
```

---

## S. Context Processors

Inject variables into **every** template automatically — no need to pass them in `render_template()`.

```python
@app.context_processor
def inject_globals():
    return {
        'app_name': 'My Flask App',
        'current_year': datetime.now().year,
        'is_admin': current_user.is_authenticated and current_user.role == 'admin',
    }
```

Now in **any** template:
```html
<footer>© {{ current_year }} {{ app_name }}</footer>
{% if is_admin %}<a href="/admin">Admin</a>{% endif %}
```

### Utility Functions in Templates

```python
@app.context_processor
def utility_processor():
    def format_price(amount, currency='₹'):
        return f'{currency}{amount:,.2f}'
    return dict(format_price=format_price)
```

```html
<p>Price: {{ format_price(999.5) }}</p>  <!-- ₹999.50 -->
```

---

## T. File Downloads / `send_file`

```python
from flask import send_file, send_from_directory

# Send a specific file
@app.route('/download/report')
def download_report():
    return send_file('reports/monthly.pdf', as_attachment=True)

# Send from a directory (safer — prevents path traversal)
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('uploads', filename, as_attachment=True)

# Send in-memory file (e.g., generated CSV)
import io
@app.route('/export')
def export_csv():
    output = io.BytesIO()
    output.write(b'name,email\nAlice,a@b.com\n')
    output.seek(0)
    return send_file(output, mimetype='text/csv',
                     as_attachment=True, download_name='users.csv')
```

---

## U. Flask Shell

Interactive Python shell with app context pre-loaded.

```bash
flask shell
```

```python
>>> app
<Flask 'app'>
>>> app.config['DEBUG']
True
```

### Auto-import models and db

```python
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
```

```bash
flask shell
>>> User.query.all()          # No need to import!
>>> db.session.add(User(...))
>>> db.session.commit()
```

---

## V. ProxyFix Middleware

**Required** when running behind a reverse proxy (Nginx, AWS ALB).

Without ProxyFix, Flask sees the proxy's IP instead of the real client IP, and `url_for(..., _external=True)` generates `http://` instead of `https://`.

```python
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app,
    x_for=1,       # Trust X-Forwarded-For (client IP)
    x_proto=1,     # Trust X-Forwarded-Proto (https)
    x_host=1,      # Trust X-Forwarded-Host
    x_prefix=1,    # Trust X-Forwarded-Prefix
)
```

---

## W. Extra Extensions (Quick Reference)

### Flask-Admin (Auto Admin Panel)

```python
# pip install flask-admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='My App', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
# Visit /admin → full CRUD interface automatically!
```

### Flask-Babel (Internationalization)

```python
# pip install flask-babel
from flask_babel import Babel, gettext as _

babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'hi', 'es'])

@app.route('/')
def index():
    return _('Hello, World!')  # Translatable string
```

### HTMX + Flask (Modern UI without JS frameworks)

```html
<!-- Load HTMX -->
<script src="https://unpkg.com/htmx.org@2.0.0"></script>

<!-- Click button → fetch HTML from Flask → swap into #result -->
<button hx-get="/api/data" hx-target="#result" hx-swap="innerHTML">
    Load Data
</button>
<div id="result"></div>
```

```python
@app.route('/api/data')
def data():
    # Return HTML fragment (not full page, not JSON)
    return '<p>Loaded dynamically!</p>'
```

HTMX lets you build dynamic UIs by returning **HTML fragments** from Flask — no React/Vue needed.

### Sentry (Error Monitoring)

```python
# pip install sentry-sdk[flask]
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn='https://your-key@sentry.io/12345',
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1,    # 10% of requests traced
)
# All unhandled exceptions are now reported to Sentry automatically
```

### Flask-DebugToolbar (Development)

```python
# pip install flask-debugtoolbar
from flask_debugtoolbar import DebugToolbarExtension

app.config['SECRET_KEY'] = 'dev'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
# Adds a debug panel to every HTML page showing:
# request info, SQL queries, templates, config, etc.
```
