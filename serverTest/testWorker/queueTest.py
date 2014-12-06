from __future__ import absolute_import
from os import path, environ
import json
import datetime
from flask import Flask, render_template, Blueprint, abort, jsonify, request, flash, session
import settings
from celery import Celery
from redis import StrictRedis
import serial
import time

app = Flask(__name__)
app.config.from_object(settings)

redis = StrictRedis(host='localhost')

def make_celery(app):
	celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    	celery.conf.update(app.config)
    	TaskBase = celery.Task
    	class ContextTask(TaskBase):
        	abstract = True
        	def __call__(self, *args, **kwargs):
            		with app.app_context():
                		return TaskBase.__call__(self, *args, **kwargs)
    	celery.Task = ContextTask
	return celery

celery = make_celery(app)

port = serial.Serial("/dev/ttyAMA0", baudrate=4800, timeout=1.0)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if redis.llen(app.config['REDIS_MENSAJES']):
            		flash('Task is already running at'+ app.config['REDIS_MENSAJES'], 'error')
        	else:
            		readSerial.delay()
            		flash('Task started at '+app.config['REDIS_MENSAJES'], 'info')
    	return render_template('index.html')
	#return 'Waiting for result...'

@celery.task(name="tasks.readSerial")
def readSerial():
	now = datetime.datetime.now()
	timeLlegada = now.strftime("%Y-%m-%d %H:%M")
	while True:
		data = port.readline()
	        if data:
			msg = {
				'time' : timeLlegada,
				'mensaje' : data[:-1]
				}
			redis.rpush(app.config['REDIS_MENSAJES'],msg)
		        time.sleep(0.1)


@celery.task(name="tasks.tail")
def tail():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	for i in range(0, 20):
       		msg = {
			'time' : timeString,
			'mensaje': 'El mensajito %s\n'%i
		}

		redis.rpush(app.config['REDIS_MENSAJES'],msg)
        	time.sleep(1)
    	#redis.delete(app.config['SECRET_KEY'])

@app.route("/test")
def startReading():
	res = readSerial.apply_async()
	tails = redis.lrange(app.config['REDIS_MENSAJES'],0,-1)
	context = {"id": res.task_id, "mensajes" : tails}
    	goto = "{}".format(context['id'])
	return jsonify(result=context)

@app.route("/test/result/<task_id>")
def show_result(task_id):
	retval = readSerial.AsyncResult(task_id).get(timeout=1.0)
    	return repr(retval)

if __name__ == "__main__":
	port = int(environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port = port, debug = True)
