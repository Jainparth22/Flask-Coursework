# Module 17 — Class-Based Views | Documentation

## Overview

Flask supports class-based views via `View` and `MethodView` for better code organization.

> 📖 **Official Docs**: [Class-Based Views](https://flask.palletsprojects.com/en/stable/views/)

---

## 1. `View` Class

```python
from flask.views import View

class MyView(View):
    def dispatch_request(self):
        return 'Hello!'

app.add_url_rule('/path', view_func=MyView.as_view('my_view'))
```

## 2. `MethodView` (REST APIs)

```python
from flask.views import MethodView

class UserAPI(MethodView):
    def get(self, user_id=None):
        if user_id is None:
            return jsonify(all_users)
        return jsonify(get_user(user_id))
    
    def post(self):
        return jsonify(create_user()), 201

# Register routes
view = UserAPI.as_view('user_api')
app.add_url_rule('/users', defaults={'user_id': None}, view_func=view, methods=['GET'])
app.add_url_rule('/users', view_func=view, methods=['POST'])
app.add_url_rule('/users/<int:user_id>', view_func=view, methods=['GET', 'PUT', 'DELETE'])
```

## 3. Decorators

```python
class ProtectedAPI(MethodView):
    decorators = [login_required, require_json]  # Applied to ALL methods
    
    def get(self): ...
```

## 4. Function vs Class-Based

| Feature | Function | Class |
|---------|----------|-------|
| Simple routes | ✅ Best | Overkill |
| REST APIs | Repetitive | ✅ Clean |
| Shared logic | Decorators | Inheritance |
| HTTP method dispatch | `if request.method == ...` | ✅ Automatic |

---

## Key Takeaways
- `View` for basic class-based views (override `dispatch_request`)
- `MethodView` maps HTTP methods to `get()`, `post()`, `put()`, `delete()` methods
- `decorators` class attribute applies to all methods
- `as_view('name')` converts class to view function
- `add_url_rule()` to register class views with URL rules
