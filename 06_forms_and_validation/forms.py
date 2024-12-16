"""
Forms Module — WTForms class definitions with validators.

Each form class represents an HTML form. Fields map to
<input> elements, and validators enforce rules.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    TextAreaField, SelectField, IntegerField, EmailField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, NumberRange,
    Optional, Regexp, ValidationError
)


# ============================================================
# 1. REGISTRATION FORM — Demonstrates many field types & validators
# ============================================================

class RegistrationForm(FlaskForm):
    """Full registration form with multiple validators per field."""
    
    # StringField → <input type="text">
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=3, max=25, message='Username must be 3-25 characters.'),
        Regexp(r'^[\w.]+$', message='Username can only contain letters, numbers, dots, and underscores.'),
    ])
    
    # EmailField → <input type="email">
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message='Please enter a valid email address.'),
    ])
    
    # PasswordField → <input type="password">
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters.'),
    ])
    
    # EqualTo validator — must match another field
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.'),
    ])
    
    # IntegerField with NumberRange
    age = IntegerField('Age', validators=[
        Optional(),
        NumberRange(min=13, max=120, message='Age must be between 13 and 120.'),
    ])
    
    # BooleanField → <input type="checkbox">
    accept_tos = BooleanField('I accept the Terms of Service', validators=[
        DataRequired(message='You must accept the Terms of Service.'),
    ])
    
    # SubmitField → <button type="submit">
    submit = SubmitField('Register')
    
    # ---- CUSTOM VALIDATOR (inline) ----
    def validate_username(self, field):
        """Custom validator — method name must be validate_<fieldname>."""
        forbidden = ['admin', 'root', 'superuser']
        if field.data.lower() in forbidden:
            raise ValidationError(f'"{field.data}" is a reserved username.')


# ============================================================
# 2. LOGIN FORM — Simple form
# ============================================================

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# ============================================================
# 3. FILE UPLOAD FORM
# ============================================================

class UploadForm(FlaskForm):
    file = FileField('Choose File', validators=[
        FileRequired(message='Please select a file.'),
        FileAllowed(['jpg', 'png', 'gif', 'pdf'], 'Only images and PDFs allowed!'),
    ])
    submit = SubmitField('Upload')


# ============================================================
# 4. CONTACT FORM — TextArea, SelectField
# ============================================================

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    
    # SelectField → <select>
    subject = SelectField('Subject', choices=[
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback'),
        ('bug', 'Bug Report'),
    ], validators=[DataRequired()])
    
    # TextAreaField → <textarea>
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=2000, message='Message must be 10-2000 characters.'),
    ])
    
    submit = SubmitField('Send Message')
