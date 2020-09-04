import os
import multiprocessing

try:
	pid_f = open('gunicorn_pid','r')
	os.system('kill  -TERM -{pid}'.format(pid=pid_f.readline()))
except Exception as exc:
	pass

bind = "127.0.0.1:8000"
workers=multiprocessing.cpu_count() * 2 + 1
timeout=1000
keepalive=10
pidfile='gunicorn_pid'
errorlog='logs/gunicorn_error.log'
accesslog='logs/gunicorn_access.log'