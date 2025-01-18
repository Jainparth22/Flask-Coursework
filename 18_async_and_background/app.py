"""
Module 18 — Async & Background Tasks
=======================================
Flask's async view support, threading for background tasks,
and Celery integration patterns.

Run:  python app.py
Visit: http://127.0.0.1:5000
"""

from flask import Flask, jsonify, request
import threading
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# In-memory task status (use Redis/DB in production)
task_results = {}


# ============================================================
# 1. ASYNC VIEWS (Flask 2.0+, requires Python 3.7+)
# ============================================================
# Flask supports async views with `async def`.
# Install: pip install flask[async]

@app.route('/async-demo')
async def async_demo():
    """Async view function — can use await."""
    import asyncio
    await asyncio.sleep(0.1)  # Non-blocking sleep
    return jsonify({
        'message': 'This was an async view!',
        'note': 'Use `pip install flask[async]` to enable',
    })


# ============================================================
# 2. BACKGROUND TASKS WITH THREADING
# ============================================================
# Simple approach for lightweight background work.
# For production, use Celery instead.

def background_task(task_id, duration):
    """Simulated background task."""
    task_results[task_id] = {'status': 'running', 'progress': 0}
    
    for i in range(1, duration + 1):
        time.sleep(1)
        task_results[task_id]['progress'] = int(i / duration * 100)
    
    task_results[task_id] = {
        'status': 'completed',
        'progress': 100,
        'result': f'Task {task_id} finished after {duration}s',
        'completed_at': datetime.now().isoformat(),
    }


@app.route('/task/start', methods=['POST'])
def start_task():
    """Start a background task."""
    task_id = f'task_{len(task_results) + 1}'
    duration = request.get_json(silent=True) or {}
    duration = duration.get('duration', 5)
    
    # Start background thread
    thread = threading.Thread(
        target=background_task,
        args=(task_id, duration),
        daemon=True,
    )
    thread.start()
    
    return jsonify({
        'task_id': task_id,
        'status': 'started',
        'check_url': f'/task/status/{task_id}',
    }), 202  # 202 Accepted


@app.route('/task/status/<task_id>')
def task_status(task_id):
    """Check background task status."""
    result = task_results.get(task_id)
    if not result:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task_id': task_id, **result})


# ============================================================
# 3. CELERY PATTERN (structure only — requires Redis/RabbitMQ)
# ============================================================
# This shows the PATTERN. To actually run Celery:
# 1. pip install celery redis
# 2. Start Redis: redis-server
# 3. Start Celery: celery -A app.celery worker --loglevel=info

"""
# --- celery_config.py ---
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# --- In app.py ---
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = make_celery(app)

@celery.task
def send_email(to, subject, body):
    # Long-running task
    import time
    time.sleep(5)  # Simulate sending
    return f'Email sent to {to}'

# --- In a view ---
@app.route('/send-email', methods=['POST'])
def trigger_email():
    result = send_email.delay('user@example.com', 'Hello', 'Body')
    return jsonify({'task_id': result.id}), 202

@app.route('/task-result/<task_id>')
def get_task_result(task_id):
    result = celery.AsyncResult(task_id)
    return jsonify({
        'task_id': task_id,
        'status': result.status,
        'result': result.result if result.ready() else None,
    })
"""


# ============================================================
# INDEX
# ============================================================

@app.route('/')
def index():
    return '''
    <h1>Module 18 — Async & Background Tasks</h1>
    <h2>Async Views</h2>
    <ul><li><a href="/async-demo">Async View Demo</a></li></ul>
    <h2>Background Tasks (Threading)</h2>
    <p>Start a task, then poll for status:</p>
    <pre>
curl -X POST -H "Content-Type: application/json" \\
     -d '{"duration": 5}' http://127.0.0.1:5000/task/start
     
curl http://127.0.0.1:5000/task/status/task_1
    </pre>
    <h2>Celery Pattern</h2>
    <p>See app.py for the Celery integration pattern (requires Redis).</p>
    '''


if __name__ == '__main__':
    app.run(debug=True)
