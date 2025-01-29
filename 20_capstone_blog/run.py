"""
Module 20 — Capstone: Blog Application
=========================================
A complete blog app using EVERYTHING from Modules 01-19:
- Application Factory (M09)
- Blueprints (M09)
- Configuration (M10)
- SQLAlchemy models with relationships (M08)
- Flask-Login authentication (M11)
- WTForms (M06)
- Flash messages (M07)
- Error handling & logging (M13)
- Templates with inheritance (M03)

Run:  pip install flask flask-sqlalchemy flask-login flask-wtf
      python run.py
Visit: http://127.0.0.1:5000
"""

from blog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
