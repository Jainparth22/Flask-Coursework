"""
Module 14 — Testing
=====================
The Flask application to test. A simple API for items.
"""

from flask import Flask, jsonify, request


def create_app(config=None):
    """Factory for creating the test app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret'
    app.config['TESTING'] = True
    
    if config:
        app.config.update(config)
    
    items = [
        {'id': 1, 'name': 'Laptop', 'price': 999.99},
        {'id': 2, 'name': 'Mouse', 'price': 29.99},
    ]
    next_id = [3]  # Mutable container for closure
    
    @app.route('/')
    def index():
        return '<h1>Test App</h1>'
    
    @app.route('/api/items')
    def get_items():
        return jsonify(items)
    
    @app.route('/api/items/<int:item_id>')
    def get_item(item_id):
        item = next((i for i in items if i['id'] == item_id), None)
        if not item:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(item)
    
    @app.route('/api/items', methods=['POST'])
    def create_item():
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'name required'}), 400
        item = {'id': next_id[0], 'name': data['name'], 'price': data.get('price', 0)}
        items.append(item)
        next_id[0] += 1
        return jsonify(item), 201
    
    @app.route('/api/items/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id):
        nonlocal items
        before = len(items)
        items = [i for i in items if i['id'] != item_id]
        if len(items) == before:
            return jsonify({'error': 'Not found'}), 404
        return '', 204
    
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
