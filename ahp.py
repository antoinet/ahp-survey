#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import sqlite3 as lite
import time
import datetime

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/survey/')
def survey():
	return render_template('survey.html')

@app.route('/save/')
def save():
	# get survey values together
	keys = ["natres_pubtrans", "natres_habitat", "natres_housing"]
	values = [ float(request.args[key]) for key in keys ]
	
	# ip address
	keys.append("remote_addr")
	values.append(request.remote_addr)

	# timestamp
	keys.append("timestamp")
	#values.append(int(time.time()))
	values.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	# construct the sql string
	sql = "INSERT INTO survey (" + ",".join(keys) + ") VALUES (" + ",".join(["?" for key in keys]) + ")"

	# execute the insert query
	con = lite.connect('db/survey.db')
	with con:
		cur = con.cursor()
		cur.execute(sql, tuple(values))
	
	return redirect(url_for('thankyou'), 302)

@app.route('/thankyou/')
def thankyou():
	return render_template('thankyou.html')

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

