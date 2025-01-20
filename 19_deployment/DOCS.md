# Module 19 — Deployment | Documentation

## Overview

Deploying Flask to production involves: a production WSGI server, a reverse proxy, environment configuration, and process management.

> 📖 **Official Docs**: [Deploying to Production](https://flask.palletsprojects.com/en/stable/deploying/)

---

## 1. Production WSGI Servers

**Never** use `app.run()` or `flask run` in production. Use a proper WSGI server.

### Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
gunicorn -w 4 --threads 2 -b 0.0.0.0:8000 "myapp:create_app()"
```

| Flag | Description |
|------|-------------|
| `-w 4` | 4 worker processes |
| `--threads 2` | 2 threads per worker |
| `-b 0.0.0.0:8000` | Bind to all interfaces on port 8000 |
| `--timeout 120` | Request timeout in seconds |
| `--access-logfile -` | Access log to stdout |

### Waitress (Windows/Cross-platform)
```bash
pip install waitress
waitress-serve --port=8000 app:app
waitress-serve --port=8000 --call "myapp:create_app"
```

---

## 2. Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /path/to/your/static;
        expires 30d;
    }
}
```

---

## 3. Environment Configuration

```python
# Production config
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']  # MUST be from env
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PREFERRED_URL_SCHEME = 'https'
```

---

## 4. Docker Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-secret
      - DATABASE_URL=sqlite:///app.db
```

---

## 5. Systemd Service (Linux)

```ini
# /etc/systemd/system/flask-app.service
[Unit]
Description=Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/app
Environment="SECRET_KEY=your-secret"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 6. Production Checklist

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` from environment variable
- [ ] WSGI server (Gunicorn/Waitress)
- [ ] Reverse proxy (Nginx)
- [ ] HTTPS enabled
- [ ] Secure cookie settings
- [ ] Database migrations applied
- [ ] Static files served by Nginx
- [ ] Logging configured
- [ ] Error monitoring (Sentry)

---

## 7. Cloud Deployment

### Heroku
```
# Procfile
web: gunicorn app:app
```

### PythonAnywhere
Upload code, set WSGI path in dashboard.

### Railway / Render / Fly.io
Follow their Python/Flask deployment docs.

---

## Key Takeaways
- Never use `flask run` in production
- Use Gunicorn (Linux) or Waitress (Windows)
- Put Nginx in front for static files and SSL
- All secrets from environment variables
- Docker for reproducible deployments
