#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import feedparser 
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# initialize app
app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='developmentkey',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


feed = feedparser.parse('http://www.eluniversal.com.mx/rss/mexico.xml')

dict = {u'Peña':u'Peña=>-43', u'México': u'México-revolucionario', 'Detenidos': u'Heróicos-militantes-detenidos','detenidos':u'Heróicos-militantes-detenidos', 'normalistas': u'Heroes-normalistas'}

for post in feed.entries:
	for k, v in dict.items():
		post.title = post.title.replace(k,v)

@app.route('/')
def show_entries():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {	
		'title' : 'HELLO!',
		'time': timeString
      }
	return render_template('show_entries.html',**feed)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Usuario Invalido'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Password invalido'
		else:
			session['logged_in'] = True
			flash('Ingreso con exito')
			return redirect(url_for('show_entries'))
		return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Saliste del sistema')
	return redirect(url_for('show_entries'))

# Fire up server
if __name__ == "__main__":
        app.run(host='0.0.0.0')
        app.port = 80
        app.run()	
