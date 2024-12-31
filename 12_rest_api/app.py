"""
Module 12 — RESTful APIs
==========================
Building REST APIs with Flask: JSON endpoints, HTTP methods,
status codes, request validation, and API versioning.

Run:  python app.py
Test: curl http://127.0.0.1:5000/api/v1/items
"""

from flask import Flask, jsonify, request, abort, url_for
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'api-secret'

# ============================================================
# IN-MEMORY DATA STORE (replace with database in production)
# ============================================================

items = [
    {'id': 1, 'name': 'Laptop', 'price': 999.99, 'in_stock': True},
    {'id': 2, 'name': 'Mouse', 'price': 29.99, 'in_stock': True},
    {'id': 3, 'name': 'Keyboard', 'price': 79.99, 'in_stock': False},
]
next_id = 4


# ============================================================
# HELPER: API KEY AUTHENTICATION
# ============================================================

API_KEYS = {'my-secret-api-key', 'test-key-123'}


def require_api_key(f):
    """Decorator to require API key in header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key not in API_KEYS:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated


# ============================================================
# REST API ENDPOINTS — /api/v1/items
# ============================================================

# --- LIST ALL (GET) ---
@app.route('/api/v1/items', methods=['GET'])
def get_items():
    """GET /api/v1/items — List all items with optional filtering.
    
    Query params:
        ?in_stock=true     — Filter by stock status
        ?min_price=50      — Minimum price
        ?max_price=500     — Maximum price
        ?page=1&per_page=2 — Pagination
    """
    result = items.copy()
    
    # Filtering
    if request.args.get('in_stock') is not None:
        in_stock = request.args.get('in_stock', '').lower() == 'true'
        result = [i for i in result if i['in_stock'] == in_stock]
    
    if request.args.get('min_price'):
        min_p = float(request.args.get('min_price', 0))
        result = [i for i in result if i['price'] >= min_p]
    
    if request.args.get('max_price'):
        max_p = float(request.args.get('max_price', float('inf')))
        result = [i for i in result if i['price'] <= max_p]
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    
    return jsonify({
        'items': result[start:end],
        'total': len(result),
        'page': page,
        'per_page': per_page,
    })


# --- GET ONE (GET) ---
@app.route('/api/v1/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """GET /api/v1/items/:id — Get a single item."""
    item = next((i for i in items if i['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item)


# --- CREATE (POST) ---
@app.route('/api/v1/items', methods=['POST'])
@require_api_key
def create_item():
    """POST /api/v1/items — Create a new item.
    
    Body (JSON):
        {"name": "Monitor", "price": 299.99, "in_stock": true}
    """
    global next_id
    
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    
    data = request.get_json()
    
    # Validation
    errors = []
    if not data.get('name'):
        errors.append('name is required')
    if data.get('price') is None:
        errors.append('price is required')
    elif not isinstance(data['price'], (int, float)):
        errors.append('price must be a number')
    if errors:
        return jsonify({'errors': errors}), 400
    
    item = {
        'id': next_id,
        'name': data['name'],
        'price': float(data['price']),
        'in_stock': data.get('in_stock', True),
    }
    items.append(item)
    next_id += 1
    
    return jsonify(item), 201, {'Location': f'/api/v1/items/{item["id"]}'}


# --- UPDATE (PUT — full replace) ---
@app.route('/api/v1/items/<int:item_id>', methods=['PUT'])
@require_api_key
def update_item(item_id):
    """PUT /api/v1/items/:id — Full update (replace)."""
    item = next((i for i in items if i['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'error': 'name and price are required for PUT'}), 400
    
    item['name'] = data['name']
    item['price'] = float(data['price'])
    item['in_stock'] = data.get('in_stock', True)
    
    return jsonify(item)


# --- PARTIAL UPDATE (PATCH) ---
@app.route('/api/v1/items/<int:item_id>', methods=['PATCH'])
@require_api_key
def patch_item(item_id):
    """PATCH /api/v1/items/:id — Partial update."""
    item = next((i for i in items if i['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.get_json()
    if 'name' in data:
        item['name'] = data['name']
    if 'price' in data:
        item['price'] = float(data['price'])
    if 'in_stock' in data:
        item['in_stock'] = data['in_stock']
    
    return jsonify(item)


# --- DELETE ---
@app.route('/api/v1/items/<int:item_id>', methods=['DELETE'])
@require_api_key
def delete_item(item_id):
    """DELETE /api/v1/items/:id — Delete an item."""
    global items
    before = len(items)
    items = [i for i in items if i['id'] != item_id]
    
    if len(items) == before:
        return jsonify({'error': 'Item not found'}), 404
    
    return '', 204  # No Content


# ============================================================
# ERROR HANDLERS (JSON responses for APIs)
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================
# INDEX
# ============================================================

@app.route('/')
def index():
    return '''
    <h1>Module 12 — RESTful APIs</h1>
    <h2>Endpoints</h2>
    <pre>
GET    /api/v1/items          — List all items
GET    /api/v1/items/:id      — Get one item
POST   /api/v1/items          — Create item (API key required)
PUT    /api/v1/items/:id      — Full update  (API key required)
PATCH  /api/v1/items/:id      — Partial update (API key required)
DELETE /api/v1/items/:id      — Delete item (API key required)
    </pre>
    <h2>Try it</h2>
    <pre>
curl http://127.0.0.1:5000/api/v1/items
curl http://127.0.0.1:5000/api/v1/items?in_stock=true
curl -X POST -H "Content-Type: application/json" -H "X-API-Key: test-key-123" \\
     -d '{"name":"Monitor","price":299.99}' http://127.0.0.1:5000/api/v1/items
    </pre>
    '''


if __name__ == '__main__':
    app.run(debug=True)
