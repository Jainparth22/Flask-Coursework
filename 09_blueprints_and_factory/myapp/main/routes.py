"""Main Blueprint Routes."""

from flask import render_template
from myapp.main import main_bp


@main_bp.route('/')
def index():
    """Homepage — registered route: / """
    return render_template('main/index.html', title='Home')


@main_bp.route('/about')
def about():
    return '<h1>About</h1><p>This app uses Blueprints!</p><a href="/">← Home</a>'


# Blueprint-specific hooks (only run for this blueprint's routes)
@main_bp.before_request
def before_main_request():
    """Runs before EVERY request handled by this blueprint."""
    pass  # Could check permissions, log access, etc.
