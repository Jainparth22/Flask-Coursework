"""
Module 17 — Class-Based Views
================================
Flask's MethodView and View classes for organized, reusable views.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, jsonify, request, render_template_string
from flask.views import View, MethodView

app = Flask(__name__)


# ============================================================
# 1. View CLASS (basic class-based view)
# ============================================================

class ShowUsers(View):
    """Basic View — override dispatch_request().
    
    Good for template-rendering views with shared logic.
    """
    
    def dispatch_request(self):
        users = [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
        ]
        return jsonify(users)

# Register with url rule
app.add_url_rule('/users-view', view_func=ShowUsers.as_view('show_users'))


# ============================================================
# 2. MethodView — HTTP method-based dispatching
# ============================================================

class ItemAPI(MethodView):
    """MethodView maps HTTP methods to class methods.
    
    GET    → get()
    POST   → post()
    PUT    → put()
    PATCH  → patch()
    DELETE → delete()
    """
    
    # In-memory store
    items = [
        {'id': 1, 'name': 'Laptop', 'price': 999},
        {'id': 2, 'name': 'Mouse', 'price': 29},
    ]
    next_id = 3
    
    def get(self, item_id=None):
        """Handle GET requests."""
        if item_id is None:
            # GET /api/items → list all
            return jsonify(self.items)
        # GET /api/items/<id> → get one
        item = next((i for i in self.items if i['id'] == item_id), None)
        if not item:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(item)
    
    def post(self):
        """Handle POST requests — create."""
        data = request.get_json()
        item = {
            'id': ItemAPI.next_id,
            'name': data.get('name', ''),
            'price': data.get('price', 0),
        }
        self.items.append(item)
        ItemAPI.next_id += 1
        return jsonify(item), 201
    
    def put(self, item_id):
        """Handle PUT requests — full update."""
        item = next((i for i in self.items if i['id'] == item_id), None)
        if not item:
            return jsonify({'error': 'Not found'}), 404
        data = request.get_json()
        item['name'] = data.get('name', item['name'])
        item['price'] = data.get('price', item['price'])
        return jsonify(item)
    
    def delete(self, item_id):
        """Handle DELETE requests."""
        ItemAPI.items = [i for i in self.items if i['id'] != item_id]
        return '', 204


# Register MethodView — two URL rules for collection and item
item_view = ItemAPI.as_view('item_api')
app.add_url_rule('/api/items', view_func=item_view,
                 defaults={'item_id': None}, methods=['GET'])
app.add_url_rule('/api/items', view_func=item_view,
                 methods=['POST'])
app.add_url_rule('/api/items/<int:item_id>', view_func=item_view,
                 methods=['GET', 'PUT', 'DELETE'])


# ============================================================
# 3. View with Decorators
# ============================================================

def require_auth(f):
    """Simple auth decorator."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            return jsonify({'error': 'Auth required'}), 401
        return f(*args, **kwargs)
    return decorated


class ProtectedView(MethodView):
    """MethodView with decorators."""
    
    # Apply decorators to ALL methods
    decorators = [require_auth]
    
    def get(self):
        return jsonify({'message': 'Secret data!'})

app.add_url_rule('/api/secret', view_func=ProtectedView.as_view('secret'))


# ============================================================
# 4. View with init_every_request
# ============================================================

class CounterView(View):
    """View that creates a new instance per request (default)
    vs sharing state across requests.
    """
    init_every_request = False  # Share state across requests
    
    def __init__(self):
        self.count = 0
    
    def dispatch_request(self):
        self.count += 1
        return jsonify({'count': self.count})

app.add_url_rule('/counter', view_func=CounterView.as_view('counter'))


# ============================================================
# INDEX
# ============================================================

@app.route('/')
def index():
    return '''
    <h1>Module 17 — Class-Based Views</h1>
    <h2>View class</h2>
    <ul><li><a href="/users-view">Show Users (View)</a></li></ul>
    <h2>MethodView (REST)</h2>
    <ul>
        <li><a href="/api/items">GET /api/items</a></li>
        <li><a href="/api/items/1">GET /api/items/1</a></li>
    </ul>
    <h2>Decorated View</h2>
    <ul><li><a href="/api/secret">GET /api/secret (needs Auth header)</a></li></ul>
    <h2>Shared State</h2>
    <ul><li><a href="/counter">Counter (increments per request)</a></li></ul>
    '''


if __name__ == '__main__':
    app.run(debug=True)
