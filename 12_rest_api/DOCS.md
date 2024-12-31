# Module 12 — RESTful APIs | Documentation

## Overview

Flask is excellent for building REST APIs. Use `jsonify()`, proper HTTP methods, status codes, and content negotiation.

> 📖 **Official Docs**: [APIs with JSON](https://flask.palletsprojects.com/en/stable/quickstart/#apis-with-json)

---

## 1. REST Principles

| Method | URL | Action | Success Code |
|--------|-----|--------|-------------|
| `GET` | `/api/items` | List all | 200 |
| `GET` | `/api/items/1` | Get one | 200 |
| `POST` | `/api/items` | Create | 201 |
| `PUT` | `/api/items/1` | Full update | 200 |
| `PATCH` | `/api/items/1` | Partial update | 200 |
| `DELETE` | `/api/items/1` | Delete | 204 |

---

## 2. JSON Responses

```python
# Method 1: jsonify()
return jsonify({'name': 'Parth'}), 200

# Method 2: Return dict (Flask 1.0+)
return {'name': 'Parth'}

# With status code
return jsonify({'created': True}), 201

# With headers
return jsonify(data), 201, {'Location': '/api/items/1'}
```

## 3. Reading JSON Input

```python
data = request.get_json()                    # Parse JSON body
data = request.get_json(force=True)          # Parse even without Content-Type
data = request.get_json(silent=True)         # Return None on failure
```

## 4. Request Validation Pattern

```python
@app.route('/api/items', methods=['POST'])
def create():
    if not request.is_json:
        return jsonify({'error': 'JSON required'}), 415
    
    data = request.get_json()
    errors = []
    if not data.get('name'):
        errors.append('name is required')
    if errors:
        return jsonify({'errors': errors}), 400
    
    # ... create item ...
    return jsonify(item), 201
```

## 5. API Versioning

```python
# URL prefix approach
@app.route('/api/v1/items')  # Version 1
@app.route('/api/v2/items')  # Version 2

# Blueprint approach (recommended)
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')
```

## 6. Error Handling for APIs

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400
```

## 7. Common Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation failed |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 415 | Unsupported Media | Wrong Content-Type |
| 500 | Server Error | Unhandled exception |

---

## Key Takeaways
- Use proper HTTP methods (GET/POST/PUT/PATCH/DELETE)
- Return appropriate status codes (201 for create, 204 for delete)
- Validate input and return 400 with error details
- Use JSON error responses (not HTML) for APIs
- API versioning via URL prefix or blueprints
