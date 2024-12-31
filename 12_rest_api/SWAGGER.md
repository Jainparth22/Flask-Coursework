# Swagger / OpenAPI in Flask

Auto-generate interactive API documentation (like Swagger UI) for your Flask APIs.

> 📖 **OpenAPI Spec**: [swagger.io/specification](https://swagger.io/specification/)

---

## Option 1: Flask-RESTX (Recommended for new APIs)

```bash
pip install flask-restx
```

```python
from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, title='My API', version='1.0',
          description='A demo API with Swagger docs')

# Namespace (like a Blueprint for APIs)
ns = api.namespace('items', description='Item operations')

# Model (defines request/response schema + Swagger docs)
item_model = api.model('Item', {
    'id': fields.Integer(readonly=True, description='Item ID'),
    'name': fields.String(required=True, description='Item name'),
    'price': fields.Float(required=True, description='Item price'),
})

@ns.route('/')
class ItemList(Resource):
    @ns.marshal_list_with(item_model)
    def get(self):
        """List all items"""
        return [{'id': 1, 'name': 'Laptop', 'price': 999}]

    @ns.expect(item_model)
    @ns.marshal_with(item_model, code=201)
    def post(self):
        """Create a new item"""
        return api.payload, 201

@ns.route('/<int:item_id>')
class ItemDetail(Resource):
    @ns.marshal_with(item_model)
    @ns.response(404, 'Item not found')
    def get(self, item_id):
        """Get item by ID"""
        return {'id': item_id, 'name': 'Laptop', 'price': 999}

    @ns.response(204, 'Item deleted')
    def delete(self, item_id):
        """Delete an item"""
        return '', 204
```

**Swagger UI** auto-available at `http://127.0.0.1:5000/`

### Key Decorators

| Decorator | Purpose |
|-----------|---------|
| `@ns.marshal_with(model)` | Define response schema |
| `@ns.expect(model)` | Define request body schema |
| `@ns.response(code, desc)` | Document response codes |
| `@ns.param('name', 'desc')` | Document URL/query params |
| `@ns.doc(security='apikey')` | Add auth requirements |

---

## Option 2: Flasgger (Add Swagger to existing code)

Best when you already have Flask routes and want to add docs without restructuring.

```bash
pip install flasgger
```

```python
from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

@app.route('/api/items/<int:item_id>')
def get_item(item_id):
    """Get item by ID
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: The item ID
    responses:
      200:
        description: An item object
        schema:
          properties:
            id:
              type: integer
            name:
              type: string
            price:
              type: number
      404:
        description: Item not found
    """
    return jsonify({'id': item_id, 'name': 'Laptop', 'price': 999})
```

**Swagger UI** at `http://127.0.0.1:5000/apidocs`

---

## Option 3: Flask-Smorest (Marshmallow-based)

Modern approach using marshmallow schemas for validation + docs.

```bash
pip install flask-smorest marshmallow
```

```python
from flask import Flask
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['API_TITLE'] = 'My API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/docs'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

blp = Blueprint('items', __name__, url_prefix='/api/items')

@blp.route('/')
class Items(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """List items"""
        return [{'id': 1, 'name': 'Laptop', 'price': 999}]

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, data):
        """Create item"""
        return data

api.register_blueprint(blp)
```

**Swagger UI** at `http://127.0.0.1:5000/docs`

---

## Comparison

| Feature | Flask-RESTX | Flasgger | Flask-Smorest |
|---------|------------|----------|---------------|
| Swagger UI | ✅ Built-in (`/`) | ✅ Built-in (`/apidocs`) | ✅ Built-in (`/docs`) |
| Approach | Class-based `Resource` | YAML in docstrings | Marshmallow schemas |
| Request validation | ✅ via `expect()` | ❌ Manual | ✅ Automatic |
| Learning curve | Medium | Low | Medium |
| Best for | New REST APIs | Adding docs to existing code | Type-safe APIs |
| OpenAPI version | 2.0 | 2.0 / 3.0 | 3.0 |

---

## Which to Choose?

- **Building a new API?** → **Flask-RESTX** (most popular, great Swagger UI)
- **Have existing routes?** → **Flasgger** (add docs with zero restructuring)
- **Want strict validation?** → **Flask-Smorest** (marshmallow auto-validates)
