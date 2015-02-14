#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as lite

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/survey/')
def survey():
	return render_template('survey.html')

@app.route('/done/')
def done():
#	save_record(**request.args)
	#return "thank you"
	s = ""
	for key,value in request.args:
		s += "%s = %s<br/>" % (key, value)
	return s

def save_record(**fields):
	con = lite.connect('db/survey.db')
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO survey (natres_pubtrans, natres_habitat, natres_housing) VALUES(?, ?, ?)", (float(fields["natres_pubtrans"]), float(fields["natres_habitat"]), float(fields["natres_housing"])))

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

