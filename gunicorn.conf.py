# gunicorn.conf.py
bind = "0.0.0.0:8000"
timeout = 120
workers = 1
threads = 1
worker_class = "sync"
max_requests = 1000
max_requests_jitter = 50
preload_app = True
