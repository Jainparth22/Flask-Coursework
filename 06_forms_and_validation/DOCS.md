# Module 06 — Forms & Validation | Documentation

## Overview

Flask-WTF integrates WTForms with Flask, providing CSRF protection, file upload handling, and seamless form validation.

> 📖 **Official Docs**: [Flask-WTF](https://flask-wtf.readthedocs.io/)  
> 📖 **WTForms Docs**: [WTForms](https://wtforms.readthedocs.io/)

---

## 1. Setup

```bash
pip install Flask-WTF
```

```python
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for CSRF
```

---

## 2. Defining Forms

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
```

### Field Types

| WTForms Field | HTML Element | Import From |
|---------------|-------------|-------------|
| `StringField` | `<input type="text">` | `wtforms` |
| `PasswordField` | `<input type="password">` | `wtforms` |
| `EmailField` | `<input type="email">` | `wtforms` |
| `IntegerField` | `<input type="number">` | `wtforms` |
| `FloatField` | `<input type="number">` | `wtforms` |
| `BooleanField` | `<input type="checkbox">` | `wtforms` |
| `TextAreaField` | `<textarea>` | `wtforms` |
| `SelectField` | `<select>` | `wtforms` |
| `FileField` | `<input type="file">` | `flask_wtf.file` |
| `SubmitField` | `<button type="submit">` | `wtforms` |
| `HiddenField` | `<input type="hidden">` | `wtforms` |
| `DateField` | `<input type="date">` | `wtforms` |

---

## 3. Built-in Validators

| Validator | Purpose | Example |
|-----------|---------|---------|
| `DataRequired()` | Field must not be empty | `validators=[DataRequired()]` |
| `Email()` | Must be valid email | `validators=[Email()]` |
| `Length(min, max)` | String length range | `Length(min=3, max=25)` |
| `EqualTo('field')` | Must match another field | `EqualTo('password')` |
| `NumberRange(min, max)` | Number range | `NumberRange(min=1, max=100)` |
| `Regexp(pattern)` | Match regex pattern | `Regexp(r'^[\w]+$')` |
| `Optional()` | Field is optional | `validators=[Optional()]` |
| `URL()` | Must be valid URL | `validators=[URL()]` |
| `AnyOf(values)` | Must be one of values | `AnyOf(['a', 'b'])` |
| `NoneOf(values)` | Must not be one of values | `NoneOf(['admin'])` |

---

## 4. Custom Validators

### Inline (method on form class)
```python
class MyForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    
    def validate_username(self, field):
        if field.data.lower() == 'admin':
            raise ValidationError('This username is reserved.')
```

### Standalone (reusable)
```python
def no_special_chars(form, field):
    if not field.data.isalnum():
        raise ValidationError('Only letters and numbers allowed.')

class MyForm(FlaskForm):
    name = StringField('Name', validators=[no_special_chars])
```

---

## 5. Rendering Forms in Templates

```html
<form method="POST" novalidate>
    {{ form.hidden_tag() }}        {# CSRF token #}
    
    <div class="form-group">
        {{ form.email.label }}
        {{ form.email(class='form-control', placeholder='Email') }}
        {% for error in form.email.errors %}
            <span class="error">{{ error }}</span>
        {% endfor %}
    </div>
    
    {{ form.submit() }}
</form>
```

### Key Template Elements
- `{{ form.hidden_tag() }}` — Renders the CSRF hidden input
- `{{ form.field_name.label }}` — Renders the `<label>`
- `{{ form.field_name() }}` — Renders the `<input>`
- `{{ form.field_name.errors }}` — List of validation error messages
- Pass HTML attributes: `{{ form.field(class='my-class', id='my-id') }}`

---

## 6. Processing Forms in Views

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # All validators passed + CSRF valid + POST request
        username = form.username.data  # Cleaned data
        # ... save to database ...
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)
```

---

## 7. CSRF Protection

Flask-WTF adds CSRF (Cross-Site Request Forgery) protection automatically:

1. Set `SECRET_KEY` in config
2. Use `{{ form.hidden_tag() }}` in templates
3. `validate_on_submit()` checks the token

> 📖 **Official Docs**: [Flask-WTF — CSRF Protection](https://flask-wtf.readthedocs.io/en/stable/csrf.html)

---

## 8. File Uploads

```python
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!'),
    ])
```

```python
from werkzeug.utils import secure_filename

if form.validate_on_submit():
    f = form.file.data
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
```

> ⚠️ **Always use `secure_filename()`** to prevent directory traversal attacks.

---

## Key Takeaways

- Flask-WTF = WTForms + CSRF protection + Flask integration
- Define form classes with fields and validators
- `form.validate_on_submit()` = POST + valid + CSRF OK
- `form.field.data` for cleaned values, `form.field.errors` for errors
- `{{ form.hidden_tag() }}` for CSRF token in templates
- Custom validators: `validate_<fieldname>(self, field)` method
- `secure_filename()` for file uploads
