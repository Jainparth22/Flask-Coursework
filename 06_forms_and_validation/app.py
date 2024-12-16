"""
Module 06 — Forms & Validation
================================
Flask-WTF for form handling, CSRF protection, field validators,
custom validators, and file uploads with secure_filename.

Run:  pip install flask-wtf
      python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, render_template, redirect, url_for, flash, request
from forms import RegistrationForm, LoginForm, UploadForm, ContactForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max upload


@app.route('/')
def index():
    return render_template('base.html', title='Forms & Validation')


# ============================================================
# 1. REGISTRATION FORM — Multiple field types & validators
# ============================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    # validate_on_submit() checks:
    #   1. Is this a POST request?
    #   2. Do all validators pass?
    #   3. Is the CSRF token valid?
    if form.validate_on_submit():
        # form.field_name.data contains the cleaned value
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html', title='Register', form=form)


# ============================================================
# 2. LOGIN FORM — Simple example
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Logged in as {form.email.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)


# ============================================================
# 3. FILE UPLOAD FORM
# ============================================================

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        # In production, always use secure_filename!
        from werkzeug.utils import secure_filename
        filename = secure_filename(form.file.data.filename)
        # form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'File "{filename}" uploaded successfully!', 'success')
        return redirect(url_for('upload'))
    return render_template('upload.html', title='Upload', form=form)


# ============================================================
# 4. CONTACT FORM — TextArea, SelectField
# ============================================================

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(f'Message from {form.name.data} received!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact', form=form)


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
