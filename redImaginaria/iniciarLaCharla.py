#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, environ
import datetime
import serial 
import time
import json
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash
from redis import StrictRedis
from celery import Celery

from assets import assets
import configuracion

# inicializando app
app = Flask(__name__)



# modulos y config para uploader

import os.path

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.storage import get_default_storage_class
from flask.ext.uploads import delete, init, save, Upload
from werkzeug import secure_filename


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.config['UPLOADED_FILES_ALLOW'] = 'jpg'
app.config['UPLOADED_FILES_DENY'] = 'png'
app.config['UPLOADS_FOLDER'] = os.path.realpath('.') + '/static/'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
db = SQLAlchemy(app)

Storage = get_default_storage_class(app)

init(db, Storage)

db.create_all()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])



def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# termina modulos y config uploader



app.config.from_object(configuracion)
assets.init_app(app)

# levantando servicio redis
redis = StrictRedis(host='localhost', decode_responses=True, encoding='utf-8')

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

#levantando servicio celery
celery = make_celery(app)

# configurndo para escuchar puerta UART
UART = serial.Serial('/dev/ttyAMA0',baudrate=4800, timeout=1.0)
if (UART.isOpen() == False):
	UART.open()
UART.flushInput()
UART.flushOutput()

@app.route('/')
def index():
	if redis.llen(app.config['REDIS_MENSAJES']):
		flash('Task is already running at'+ app.config['REDIS_MENSAJES'], 'error')
	else:
		readSerial.delay()
		flash('Task started at '+app.config['REDIS_MENSAJES'], 'info')


	if request.method == 'POST':
		print 'saving'

		file = request.files['upload']

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			save(request.files['upload'])


		return redirect(url_for('index'))

	uploads = reversed(Upload.query.all())
	return render_template('index.html', uploads=uploads)

#	return render_template('index.html')

#Creando task para leer serial
@celery.task(name="tasks.readSerial")
def readSerial():
	while True:
		data = UART.readline()
		if data:
			rxnow = datetime.datetime.now()
			horaRecepcion = rxnow.strftime("%Y-%m-%d %H:%M:%S")
			print("r: "+data)
			msg = {
				"time" : horaRecepcion,
				"mensaje" : data
				}
			redis.rpush(app.config['REDIS_MENSAJES'],msg)
			time.sleep(0.1)
		time.sleep(0.1)




#Creando ruta para enviar mensajes
@app.route('/_conversar', methods=['POST'])
def enviarMensaje():
	txnow = datetime.datetime.now()
	timeString = txnow.strftime("%Y-%m-%d %H:%M:%S")
	mensaje = request.form.get('mensaje')
	#mensaje = mensaje+'\n'
	UART.write(mensaje.encode('UTF-8'))
        mensajeTX = {
                "mensaje" : mensaje,
                "time": timeString
      	}
	return jsonify(mensajeTX)	

#Creando ruta para leer la cola de mensajes
@app.route("/_mensajes")
def leerCola():
	res = readSerial.apply_async()
	tails = redis.lrange(app.config['REDIS_MENSAJES'],0,-1)
	jsonDeMensajes = {"id": res.task_id, "mensajes" : tails}
	return jsonify(result = jsonDeMensajes, encoding='utf-8')





@app.route('/delete/<int:id>', methods=['POST'])
def remove(id):
    upload = Upload.query.get_or_404(id)
    delete(upload)
    return redirect(url_for('index'))



@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        print 'saving'

        file = request.files['upload']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save(request.files['upload'])

        return redirect(url_for('index'))

    uploads = reversed(Upload.query.all())
    return render_template('index.html', uploads=uploads)





# Correr el server
if __name__ == "__main__":
        port = int(environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port = port, debug = True)
