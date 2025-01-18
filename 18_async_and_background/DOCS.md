# Module 18 — Async & Background Tasks | Documentation

## Overview

Flask 2.0+ supports `async def` views. For long-running tasks, use threading or Celery.

> 📖 **Official Docs**: [Async/Await](https://flask.palletsprojects.com/en/stable/async-await/)

---

## 1. Async Views (Flask 2.0+)

```bash
pip install flask[async]
```

```python
@app.route('/async')
async def async_view():
    data = await some_async_function()
    return jsonify(data)
```

> ⚠️ Flask runs async views in a thread by default. For true async performance, use `hypercorn` or `uvicorn` as your server.

---

## 2. Background Tasks (Threading)

```python
import threading

def background_work(task_id):
    time.sleep(10)  # Long operation
    results[task_id] = 'done'

@app.route('/start')
def start():
    t = threading.Thread(target=background_work, args=('task_1',), daemon=True)
    t.start()
    return jsonify({'status': 'started'}), 202
```

---

## 3. Celery (Production)

```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def send_email(to, subject):
    # Long-running task
    ...

# Trigger
result = send_email.delay('user@example.com', 'Hello')
result.id       # Task ID
result.status   # PENDING, STARTED, SUCCESS, FAILURE
result.result   # Return value (when done)
```

### Celery Commands
```bash
celery -A app.celery worker --loglevel=info
celery -A app.celery beat  # For scheduled tasks
```

---

## Key Takeaways
- `async def` views work in Flask 2.0+ (install `flask[async]`)
- Threading: simple but limited — good for development
- Celery: production-grade — requires Redis/RabbitMQ message broker
- Always return `202 Accepted` for async task endpoints
