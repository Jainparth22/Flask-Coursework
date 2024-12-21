"""
Module 08 — Database (Raw SQLite)
===================================
Using SQLite3 directly with Flask's g object and teardown_appcontext.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

import sqlite3
from flask import Flask, g, request, jsonify

app = Flask(__name__)
DATABASE = 'database.db'


# ============================================================
# 1. DATABASE CONNECTION MANAGEMENT
# ============================================================

def get_db():
    """Get a database connection for the current request.
    
    Uses Flask's `g` object to store the connection per-request.
    g is a per-request namespace — it exists for the duration
    of one request and is unique to that request.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Return rows as dict-like objects
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Close DB connection at the end of each request.
    
    teardown_appcontext runs after every request, even if an error occurred.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ============================================================
# 2. INITIALIZING THE DATABASE
# ============================================================

def init_db():
    """Create tables from schema.sql."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.executescript(f.read())
    db.commit()


@app.cli.command('init-db')
def init_db_command():
    """Flask CLI command: flask init-db"""
    init_db()
    print('Database initialized.')


# ============================================================
# 3. HELPER FUNCTION
# ============================================================

def query_db(query, args=(), one=False):
    """Execute a query and return results.
    
    Args:
        query: SQL query string
        args: Query parameters (use ? placeholders)
        one: If True, return only the first result
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# ============================================================
# 4. ROUTES (CRUD)
# ============================================================

@app.route('/')
def index():
    """List all users."""
    users = query_db('SELECT * FROM users ORDER BY created_at DESC')
    return jsonify([dict(u) for u in users])


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'name and email required'}), 400
    
    db = get_db()
    db.execute(
        'INSERT INTO users (name, email) VALUES (?, ?)',
        (data['name'], data['email'])
    )
    db.commit()
    return jsonify({'message': f'User {data["name"]} created'}), 201


@app.route('/users/<int:user_id>')
def get_user(user_id):
    """Get a single user by ID."""
    user = query_db('SELECT * FROM users WHERE id = ?', (user_id,), one=True)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(user))


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    return jsonify({'message': 'User deleted'})


# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Auto-create tables on first run
    app.run(debug=True)
