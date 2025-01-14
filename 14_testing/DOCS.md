# Module 14 — Testing | Documentation

## Overview

Flask provides a test client that simulates requests without running a server.

> 📖 **Official Docs**: [Testing Flask Applications](https://flask.palletsprojects.com/en/stable/testing/)

---

## 1. Setup (pytest)

```bash
pip install pytest
```

## 2. Test Client

```python
@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    return app.test_client()
```

### Making Requests
```python
response = client.get('/api/items')            # GET
response = client.post('/api/items', json={...}) # POST with JSON
response = client.put('/api/items/1', json={...}) # PUT
response = client.delete('/api/items/1')         # DELETE
response = client.get('/', headers={'X-Key': 'val'})  # Custom headers
```

### Reading Responses
```python
response.status_code        # 200, 404, etc.
response.data                # Raw bytes
response.get_json()          # Parsed JSON
response.content_type        # 'application/json'
response.headers              # Response headers
```

## 3. Testing Contexts

```python
# App context
with app.app_context():
    assert app.config['TESTING']

# Request context (without HTTP)
with app.test_request_context('/path?key=val'):
    assert request.args['key'] == 'val'
```

## 4. Running Tests

```bash
pytest test_app.py -v          # Verbose output
pytest test_app.py -k "test_get"  # Run matching tests
pytest --tb=short              # Short tracebacks
```

---

## Key Takeaways
- `app.test_client()` simulates HTTP requests (no server needed)
- Use `json=` parameter for JSON POST requests
- `response.get_json()` to parse JSON responses
- Fixtures enable fresh app/client per test
- `TESTING=True` disables error catching for clearer test failures
