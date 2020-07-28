from flask import Flask
import redis
from rq import Queue, Worker
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678910'
r = redis.Redis(host='redis')
#r = redis.Redis()
que = Queue(connection=r)
worker = Worker(que)

subprocess.Popen(['rqworker', "--url", "redis://redis:6379"])

import catdog.routes