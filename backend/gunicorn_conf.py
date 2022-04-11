from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/srv/tranquility/socket/gunicorn.sock'

# Worker Options
workers = cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/var/log/tranquility/access_log'
errorlog = '/var/log/tranquility/error_log'
