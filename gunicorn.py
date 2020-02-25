from app.utils.config import get_config

bind = "0.0.0.0:5000"
workers = get_config('GUNICORN_WORKERS')
threads = get_config('GUNICORN_THREADS')
