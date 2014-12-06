#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import feedparser
import serial 
import time
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash

# initialize app
app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='developmentkey',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

port = serial.Serial('/dev/ttyAMA0')
if (port.isOpen() == False):
    port.open()

port.flushInput()
port.flushOutput()

#feed = feedparser.parse('http://www.eluniversal.com.mx/rss/mexico.xml')

#dict = {u'Peña':u'Peña=>-43', u'México': u'México-revolucionario', 'Detenidos': u'Heróicos-militantes-detenidos','detenidos':u'Heróicos-militantes-detenidos', 'normalistas': u'Heroes-normalistas'}

#for post in feed.entries:
#	for k, v in dict.items():
#		post.title = post.title.replace(k,v)

@app.route('/')
def iniciar():
#	return render_template('index.html',**feed)
	return render_template('index.html')

@app.route('/_conversar')
def mandarMensaje():
	now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
	mensaje = request.args.get('mensaje')
	mensaje = mensaje+'\n'
	port.write(mensaje.encode('UTF-8'))
	#time.sleep(0.05)
        mensajeTX = {
                'mensaje' : mensaje,
                'time': timeString
      	}
	return jsonify(mensajeTX)	

def leerMensajes():
	bufferDeMensajes = ''
	while True: 
		mensaje = port.readline()
		if mensaje:
			print(mensaje)
			bufferDeMensajes = bufferDeMensajes + mensaje
		time.sleep(0.05)
	return bufferDeMensajes	



@app.route('/_recibir')
def recibirMensaje():
	now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
	mensaje = 'NaN'
	if leerMensajes() != '':
		mensaje = bufferDeMensajes.decode('UTF-8')
		bufferDeMensajes = ''	
	#while True:
	#	mensaje = port.readline()
	#	if mensaje:
	#		mensajeRX = {
	#			'mensaje' : mensaje,
	#			'time' : timeString
	#		}
	#	else :
	#		mensajeRX = {
         #                       'mensaje' : '0000',
          #                      'time' : timeString
           #             }
	#	time.sleep(0.05)
	return jsonify(mensaje=mensaje)
# Fire up server
if __name__ == "__main__":
        app.run(host='0.0.0.0')
        app.port = 80
        app.run()	
