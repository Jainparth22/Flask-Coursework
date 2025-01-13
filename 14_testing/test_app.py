"""
Module 14 — Testing Flask Applications
=========================================
Using pytest with Flask's test client.

Run:  pip install pytest
      pytest test_app.py -v
"""

import pytest
from app import create_app


# ============================================================
# 1. FIXTURES — Setup for tests
# ============================================================

@pytest.fixture
def app():
    """Create a test app instance."""
    app = create_app({'TESTING': True})
    return app


@pytest.fixture
def client(app):
    """Flask test client — simulates HTTP requests.
    
    No need to run a server! The test client sends requests directly
    to the application.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI test runner — for testing Flask CLI commands."""
    return app.test_cli_runner()


# ============================================================
# 2. BASIC TESTS
# ============================================================

class TestBasic:
    """Basic application tests."""
    
    def test_app_exists(self, app):
        """App should be created."""
        assert app is not None
    
    def test_app_is_testing(self, app):
        """App should be in testing mode."""
        assert app.config['TESTING'] is True
    
    def test_index(self, client):
        """GET / should return 200."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Test App' in response.data


# ============================================================
# 3. API TESTS — CRUD operations
# ============================================================

class TestItemsAPI:
    """Test the Items API endpoints."""
    
    def test_get_all_items(self, client):
        """GET /api/items should return list of items."""
        response = client.get('/api/items')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 2
    
    def test_get_single_item(self, client):
        """GET /api/items/1 should return one item."""
        response = client.get('/api/items/1')
        assert response.status_code == 200
        item = response.get_json()
        assert item['id'] == 1
        assert 'name' in item
    
    def test_get_nonexistent_item(self, client):
        """GET /api/items/999 should return 404."""
        response = client.get('/api/items/999')
        assert response.status_code == 404
    
    def test_create_item(self, client):
        """POST /api/items should create a new item."""
        response = client.post('/api/items',
            json={'name': 'Tablet', 'price': 499.99}
        )
        assert response.status_code == 201
        item = response.get_json()
        assert item['name'] == 'Tablet'
        assert item['price'] == 499.99
        assert 'id' in item
    
    def test_create_item_missing_name(self, client):
        """POST /api/items without name should return 400."""
        response = client.post('/api/items', json={'price': 100})
        assert response.status_code == 400
    
    def test_delete_item(self, client):
        """DELETE /api/items/1 should return 204."""
        response = client.delete('/api/items/1')
        assert response.status_code == 204
        
        # Verify it's gone
        response = client.get('/api/items/1')
        assert response.status_code == 404
    
    def test_delete_nonexistent(self, client):
        """DELETE /api/items/999 should return 404."""
        response = client.delete('/api/items/999')
        assert response.status_code == 404


# ============================================================
# 4. TEST CLIENT FEATURES
# ============================================================

class TestClientFeatures:
    """Demonstrate test client capabilities."""
    
    def test_json_request(self, client):
        """Send JSON data with json= parameter."""
        response = client.post('/api/items',
            json={'name': 'Phone', 'price': 799}
        )
        assert response.status_code == 201
    
    def test_headers(self, client):
        """Send custom headers."""
        response = client.get('/api/items',
            headers={'X-Custom-Header': 'test'}
        )
        assert response.status_code == 200
    
    def test_query_string(self, client):
        """Access with query parameters."""
        response = client.get('/api/items?page=1')
        assert response.status_code == 200
    
    def test_response_data(self, client):
        """Access response data in different formats."""
        response = client.get('/api/items')
        
        # Raw bytes
        assert isinstance(response.data, bytes)
        
        # JSON (for JSON responses)
        json_data = response.get_json()
        assert json_data is not None
        
        # Status code
        assert response.status_code == 200
        
        # Content-Type header
        assert 'application/json' in response.content_type


# ============================================================
# 5. TESTING WITH CONTEXT
# ============================================================

class TestContext:
    """Test application context features."""
    
    def test_app_context(self, app):
        """Access app inside app context."""
        with app.app_context():
            assert app.config['TESTING'] is True
    
    def test_request_context(self, app):
        """Access request inside request context."""
        with app.test_request_context('/api/items?page=2'):
            from flask import request
            assert request.path == '/api/items'
            assert request.args.get('page') == '2'
