"""
Module 09 — Blueprints & Application Factory
===============================================
Entry point — imports the app from the factory and runs it.

Run:  python run.py
Visit: http://127.0.0.1:5000
"""

from myapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
