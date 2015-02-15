#!/usr/bin/env python

from flask import Flask, request, render_template, url_for, redirect, session, make_response
import sqlite3 as lite
import time
import datetime
import random
import string
from utils import *
import definitions
import csv
import StringIO

app = Flask(__name__)
app.secret_key = '\xdfS\x03D\xe0\x93~\x0bo\x82\\\xde\xe6\xaa\x02\xd3\xcdz\xcdg\xc9\xd1r\x92'


@app.before_request
def init_session():
    if not 'sid' in session:
        sid = generate_random_string(32)
        session['sid'] = sid
    print session['sid']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/goals/', methods=['GET', 'POST'])
def goals():
    if request.method == 'POST':
        save('goals', definitions.goals)
        return redirect(url_for('natres'), 302)
    else:
        return render_template('goals.html')

@app.route('/natres/', methods=['GET', 'POST'])
def natres():
    if request.method == 'POST':
        save('natres', definitions.natres)
        return redirect(url_for('pubtrans'), 302)
    else:
        return render_template('natres.html')

@app.route('/pubtrans/', methods=['GET', 'POST'])
def pubtrans():
    if request.method == 'POST':
        save('pubtrans', definitions.pubtrans)
        return redirect(url_for('lifequality'), 302)
    else:
        return render_template('pubtrans.html')

@app.route('/lifequality/', methods=['GET', 'POST'])
def lifequality():
    if request.method == 'POST':
        save('lifequality', definitions.lifequality)
        return redirect(url_for('housing'), 302)
    else:
        return render_template('lifequality.html')

@app.route('/housing/', methods=['GET', 'POST'])
def housing():
    if request.method == 'POST':
        save('housing', definitions.housing)
        return redirect(url_for('recreation'), 302)
    else:
        return render_template('housing.html')

@app.route('/recreation/', methods=['GET', 'POST'])
def recreation():
    if request.method == 'POST':
        save('recreation', definitions.recreation)
        return redirect(url_for('confirm'), 302)
    else:
        return render_template('recreation.html')

@app.route('/confirm/', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        session.pop('sid', None)
        return redirect(url_for('thankyou'), 302)
    else:
        return render_template('confirm.html')

@app.route('/thankyou/')
def thankyou():
    return render_template('thankyou.html')

@app.route('/dump/')
def dump():
    con = lite.connect('db/survey.db')
    dict = {}
    with con:
        for table in ['goals', 'natres', 'pubtrans', 'lifequality', 'housing', 'recreation']:
            cur = con.cursor()
            cur.execute("SELECT * FROM %s" % table)
            dict[table] = {'headers': [i[0] for i in cur.description], 'values': cur.fetchall()}
    return render_template('dump.html', results=dict)

@app.route('/export/')
def export():
    table = request.args.get('table')
    if table in ['goals', 'natres', 'pubtrans', 'lifequality', 'housing', 'recreation']:
        con = lite.connect('db/survey.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM %s" % table)
            si = StringIO.StringIO()
            csvwriter = csv.writer(si)
            si.write('#')
            csvwriter.writerow([i[0] for i in cur.description]) # write headers
            csvwriter.writerows(cur)
            output = make_response(si.getvalue())
            output.headers['Content-Disposition'] = "attachment; filename=%s.csv" % (table + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            output.headers['Content-type'] = "text/csv"
            return output
    return render_template('export.html')

def save(table, fields):
    # convert values to float, default to -1 if value not existant
    keys = generate_pairs('_', *fields)
    values = [ float(request.form[key]) for key in keys ]
    
    # ip address
    keys.append("remote_addr")
    values.append(request.remote_addr)
    
    # timestamp
    keys.append("timestamp")
    #values.append(int(time.time()))
    values.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # session id
    keys.append("session_id")
    values.append(session['sid'])
    
    # construct the sql string
    #sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, ','.join(keys), ','.join(['?' for key in keys]))
    sql = "INSERT OR REPLACE INTO %s (id, %s) VALUES ((SELECT id from %s WHERE session_id = '%s'), %s)" % (table, ','.join(keys), table, session['sid'], ','.join(['?' for key in keys]))
    
    # execute the insert query
    con = lite.connect('db/survey.db')
    with con:
        cur = con.cursor()
        cur.execute(sql, tuple(values))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

