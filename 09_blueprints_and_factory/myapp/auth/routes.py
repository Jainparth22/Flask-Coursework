"""Auth Blueprint Routes."""

from flask import render_template, redirect, url_for, flash, session, request
from myapp.auth import auth_bp


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page — route: /auth/login (because of url_prefix)."""
    if request.method == 'POST':
        username = request.form.get('username', '')
        if username:
            session['user'] = username
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Login')


@auth_bp.route('/register')
def register():
    """Register page."""
    return '<h1>Register</h1><p>Registration form would go here.</p><a href="/">← Home</a>'


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.index'))
