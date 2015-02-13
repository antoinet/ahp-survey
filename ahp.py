#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/survey/')
def survey():
	print "***: ",  request.args.get('natres_pubtrans', 'n/a')
	return render_template('survey.html')

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

