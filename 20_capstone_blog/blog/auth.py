"""Auth Blueprint — registration, login, logout."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from blog.extensions import db
from blog.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        u = request.form['username']
        e = request.form['email']
        p = request.form['password']
        if User.query.filter_by(username=u).first():
            flash('Username taken.', 'error')
        elif User.query.filter_by(email=e).first():
            flash('Email taken.', 'error')
        else:
            user = User(username=u, email=e)
            user.set_password(p)
            db.session.add(user)
            db.session.commit()
            flash('Account created!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user, remember='remember' in request.form)
            flash('Welcome!', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid credentials.', 'error')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('main.index'))
