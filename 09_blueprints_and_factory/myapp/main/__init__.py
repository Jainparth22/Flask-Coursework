"""Main Blueprint — public-facing pages."""

from flask import Blueprint

# Create a Blueprint
# Args:
#   'main'         — Blueprint name (used in url_for: 'main.index')
#   __name__       — Import name (for locating templates/static)
#   template_folder — Blueprint-specific templates directory
main_bp = Blueprint('main', __name__, template_folder='templates')

# Import routes AFTER creating the blueprint to avoid circular imports
from myapp.main import routes  # noqa: E402, F401
