"""
Module 07 — Cookies, Sessions & Message Flashing
===================================================
Cookies (set/read/delete with options), signed sessions,
flash messages with categories.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

from flask import (
    Flask, session, request, redirect, url_for,
    flash, get_flashed_messages, make_response,
    render_template
)
from datetime import timedelta

app = Flask(__name__)

# SECRET_KEY is REQUIRED for sessions (signs the session cookie)
app.config['SECRET_KEY'] = 'change-this-in-production-use-os-urandom'

# Session configuration
app.config['SESSION_COOKIE_HTTPONLY'] = True     # Block JS access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Default: 31 days


# ============================================================
# HOMEPAGE
# ============================================================

@app.route('/')
def index():
    return render_template('index.html',
        title='Cookies, Sessions & Flashing',
        username=session.get('username'),
        theme=request.cookies.get('theme', 'light'),
    )


# ============================================================
# 1. COOKIES — Low-level HTTP cookies
# ============================================================

@app.route('/cookie/set')
def set_cookie():
    """Set cookies with various options."""
    resp = make_response(redirect(url_for('index')))
    
    # Basic cookie
    resp.set_cookie('theme', 'dark')
    
    # Cookie with all options
    resp.set_cookie(
        'preferences',              # name
        'lang=en;tz=UTC',           # value
        max_age=60*60*24*30,        # 30 days in seconds
        expires=None,               # Alternative: datetime object
        path='/',                   # Cookie path scope
        domain=None,                # Cookie domain scope
        secure=False,               # True = HTTPS only
        httponly=True,               # True = no JS access
        samesite='Lax',             # 'Strict', 'Lax', or 'None'
    )
    
    flash('Cookies set! (theme=dark, preferences=lang=en;tz=UTC)', 'success')
    return resp


@app.route('/cookie/read')
def read_cookie():
    """Read cookies from the request."""
    theme = request.cookies.get('theme', 'not set')
    preferences = request.cookies.get('preferences', 'not set')
    
    # Get ALL cookies
    all_cookies = {k: v for k, v in request.cookies.items()}
    
    flash(f'theme={theme}, preferences={preferences}', 'info')
    return redirect(url_for('index'))


@app.route('/cookie/delete')
def delete_cookie():
    """Delete cookies."""
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('theme')
    resp.delete_cookie('preferences')
    flash('Cookies deleted!', 'warning')
    return resp


# ============================================================
# 2. SESSIONS — Server-signed cookies
# ============================================================
# Sessions store data in a signed cookie (tamper-proof but readable).
# The data is serialized to JSON, signed with SECRET_KEY.
# Max size: ~4KB (cookie limit).

@app.route('/session/login', methods=['GET', 'POST'])
def session_login():
    """Set session data (simulated login)."""
    if request.method == 'POST':
        username = request.form.get('username', 'Guest')
        
        # Set session values (like a dict)
        session['username'] = username
        session['role'] = 'user'
        session['login_count'] = session.get('login_count', 0) + 1
        
        # Make session permanent (uses PERMANENT_SESSION_LIFETIME)
        session.permanent = True
        
        flash(f'Welcome, {username}! (Login #{session["login_count"]})', 'success')
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Login')


@app.route('/session/read')
def session_read():
    """Read session data."""
    if 'username' in session:
        data = {
            'username': session['username'],
            'role': session.get('role', 'unknown'),
            'login_count': session.get('login_count', 0),
            'permanent': session.permanent,
        }
        flash(f'Session data: {data}', 'info')
    else:
        flash('No session data. Please login first.', 'warning')
    return redirect(url_for('index'))


@app.route('/session/modify')
def session_modify():
    """Modify session data — must mark as modified for mutable objects."""
    if 'username' in session:
        session['role'] = 'admin'  # Direct assignment auto-marks as modified
        
        # For nested mutable objects, you must mark manually:
        # session.modified = True
        
        flash('Session role changed to admin!', 'success')
    else:
        flash('No active session.', 'warning')
    return redirect(url_for('index'))


@app.route('/session/logout')
def session_logout():
    """Clear session data (logout)."""
    username = session.get('username', 'Guest')
    
    # Method 1: Clear specific keys
    # session.pop('username', None)
    
    # Method 2: Clear ALL session data
    session.clear()
    
    flash(f'Goodbye, {username}! Session cleared.', 'info')
    return redirect(url_for('index'))


# ============================================================
# 3. MESSAGE FLASHING
# ============================================================
# flash() stores a message for the NEXT request (uses session internally).
# get_flashed_messages() retrieves and clears them.

@app.route('/flash/demo')
def flash_demo():
    """Demonstrate different flash message categories."""
    flash('This is a success message.', 'success')
    flash('This is an info message.', 'info')
    flash('This is a warning message.', 'warning')
    flash('This is an error message.', 'error')
    flash('This is a message with no category.')  # Default category: 'message'
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
