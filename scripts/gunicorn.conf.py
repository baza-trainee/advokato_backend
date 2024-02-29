from multiprocessing import cpu_count
import os

bind = f"0.0.0.0:{os.environ.get('FLASK_PORT')}"
worker_class = "gevent"
workers = (cpu_count() * 2) + 1
loglevel = "warning"
worker_connections = 1000
