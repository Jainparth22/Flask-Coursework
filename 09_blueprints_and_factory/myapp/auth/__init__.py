"""Auth Blueprint — authentication-related pages."""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates')

from myapp.auth import routes  # noqa: E402, F401
