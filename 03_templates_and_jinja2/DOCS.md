# Module 03 — Templates & Jinja2 | Documentation

## Overview

Flask uses **Jinja2** as its template engine. Templates are HTML files with special syntax that lets you insert dynamic data, use logic (loops, conditions), and build reusable layouts.

> 📖 **Official Docs**: [Templates](https://flask.palletsprojects.com/en/stable/templating/)  
> 📖 **Jinja2 Docs**: [Template Designer Documentation](https://jinja.palletsprojects.com/en/stable/templates/)

---

## 1. Rendering Templates

```python
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', title='Home', items=[1, 2, 3])
```

Flask looks for templates in a `templates/` folder by default (relative to `app.py`).

---

## 2. Jinja2 Syntax Delimiters

| Syntax | Purpose | Example |
|--------|---------|---------|
| `{{ ... }}` | Output a variable/expression | `{{ user.name }}` |
| `{% ... %}` | Execute statements (if, for, block) | `{% if logged_in %}` |
| `{# ... #}` | Comments (not in output) | `{# TODO: fix this #}` |

---

## 3. Template Inheritance

The most powerful Jinja2 feature. Define a **base template** with `{% block %}` placeholders, then **extend** it in child templates.

### Base Template (`base.html`)
```html
<!DOCTYPE html>
<html>
<head><title>{% block title %}Default{% endblock %}</title></head>
<body>
    <nav>...</nav>
    {% block content %}{% endblock %}
    <footer>...</footer>
</body>
</html>
```

### Child Template
```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>Hello!</h1>
{% endblock %}
```

### Key Rules
- `{% extends %}` must be the **first tag** in the file
- Use `{{ super() }}` to include the parent block's content
- Blocks can be nested and named anything

> 📖 **Official Docs**: [Jinja2 — Template Inheritance](https://jinja.palletsprojects.com/en/stable/templates/#template-inheritance)

---

## 4. Control Structures

### Conditionals
```html
{% if user %}
    <p>Hello, {{ user.name }}!</p>
{% elif guest %}
    <p>Hello, Guest!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}
```

### For Loops
```html
{% for item in items %}
    <li>{{ item }}</li>
{% else %}
    <li>No items found.</li>
{% endfor %}
```

### Loop Variables
| Variable | Description |
|----------|-------------|
| `loop.index` | Current iteration (1-based) |
| `loop.index0` | Current iteration (0-based) |
| `loop.first` | `True` on first iteration |
| `loop.last` | `True` on last iteration |
| `loop.length` | Total items |
| `loop.revindex` | Reverse index (1-based) |
| `loop.cycle('odd', 'even')` | Alternate values |

---

## 5. Filters

Transform data with `{{ value|filter }}`:

### Common Built-in Filters
| Filter | Example | Result |
|--------|---------|--------|
| `upper` | `{{ "hello"\|upper }}` | `HELLO` |
| `lower` | `{{ "HELLO"\|lower }}` | `hello` |
| `title` | `{{ "hello world"\|title }}` | `Hello World` |
| `capitalize` | `{{ "hello"\|capitalize }}` | `Hello` |
| `trim` | `{{ " hi "\|trim }}` | `hi` |
| `length` | `{{ [1,2,3]\|length }}` | `3` |
| `join` | `{{ [1,2,3]\|join(", ") }}` | `1, 2, 3` |
| `sort` | `{{ [3,1,2]\|sort }}` | `[1, 2, 3]` |
| `default` | `{{ x\|default("N/A") }}` | `N/A` (if x undefined) |
| `truncate` | `{{ text\|truncate(20) }}` | First 20 chars + `...` |
| `round` | `{{ 3.14159\|round(2) }}` | `3.14` |
| `int` | `{{ "42"\|int }}` | `42` |
| `striptags` | `{{ "<b>hi</b>"\|striptags }}` | `hi` |
| `replace` | `{{ "Hi World"\|replace("World","Flask") }}` | `Hi Flask` |

### Custom Filters
```python
@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]
```
Usage: `{{ "hello"|reverse_string }}` → `olleh`

### Chaining Filters
`{{ "hello world"|title|reverse_string }}` → `dlroW olleH`

> 📖 **Official Docs**: [Jinja2 — Builtin Filters](https://jinja.palletsprojects.com/en/stable/templates/#builtin-filters)

---

## 6. Macros (Reusable Components)

Like functions but for templates:

```html
{# Define in macros.html #}
{% macro alert(message, type='info') %}
    <div class="alert alert-{{ type }}">{{ message }}</div>
{% endmacro %}

{# Use in another template #}
{% from "macros.html" import alert %}
{{ alert("Success!", "success") }}
```

> 📖 **Official Docs**: [Jinja2 — Macros](https://jinja.palletsprojects.com/en/stable/templates/#macros)

---

## 7. Context Processors

Inject variables into **every** template automatically:

```python
@app.context_processor
def inject_globals():
    return {'app_name': 'My App', 'year': 2025}
```

Now `{{ app_name }}` and `{{ year }}` are available in all templates without passing them explicitly.

> 📖 **Official Docs**: [Context Processors](https://flask.palletsprojects.com/en/stable/templating/#context-processors)

---

## 8. Autoescaping

Jinja2 **automatically escapes** HTML in `{{ }}` to prevent XSS attacks:

```python
# In Python
name = '<script>alert("XSS")</script>'

# In template: {{ name }}
# Output: &lt;script&gt;alert("XSS")&lt;/script&gt;  (safe!)
```

To insert trusted HTML, use the `|safe` filter or `Markup()`:
```html
{{ trusted_html|safe }}
```

> 📖 **Official Docs**: [Controlling Autoescaping](https://flask.palletsprojects.com/en/stable/templating/#controlling-autoescaping)

---

## Key Takeaways

- `render_template('file.html', key=value)` renders templates with data
- `{% extends "base.html" %}` + `{% block %}` = template inheritance
- `{{ variable|filter }}` transforms output (chain with `|`)
- `{% if %}`, `{% for %}` for logic; `loop.index`, `loop.first` for loop info
- Macros = reusable template components
- Context processors inject global template variables
- Autoescaping prevents XSS by default
