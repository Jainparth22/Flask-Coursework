"""
SQLAlchemy Models — User and Post with a one-to-many relationship.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class User(db.Model):
    """User model — demonstrates column types, constraints, and relationships."""
    
    __tablename__ = 'users'  # Explicit table name (optional, defaults to class name lowercase)
    
    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text, default='')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # --- Relationship ---
    # One user has many posts (one-to-many)
    # backref creates a reverse reference: post.author → User
    # lazy='dynamic' returns a query object instead of loading all posts
    # cascade='all, delete-orphan' deletes posts when user is deleted
    posts = db.relationship('Post', backref='author', lazy='select',
                           cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'post_count': len(self.posts),
        }


class Post(db.Model):
    """Post model — belongs to a User."""
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Foreign key — links to users.id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id,
        }


# ============================================================
# COLUMN TYPES REFERENCE
# ============================================================
# db.Integer        → INTEGER
# db.String(n)      → VARCHAR(n)
# db.Text           → TEXT (unlimited length)
# db.Float          → FLOAT
# db.Boolean        → BOOLEAN
# db.DateTime       → DATETIME
# db.Date           → DATE
# db.Time           → TIME
# db.LargeBinary    → BLOB
# db.JSON           → JSON (SQLite 3.9+)
# db.Enum           → ENUM
# ============================================================
