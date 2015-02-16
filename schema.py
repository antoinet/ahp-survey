#!/usr/bin/env python

import sqlite3 as lite
import definitions
from utils import *

def create_table (name, *fields):
    sql = """CREATE TABLE %s (
        id INTEGER NOT NULL PRIMARY KEY,
        remote_addr VARCHAR(255),
        timestamp DATETIME,
        session_id VARCHAR(255),
        %s
    );""" % (name, ",\n".join(["%s VARCHAR(255)" % f for f in fields]))
    return sql

con = lite.connect('db/survey.db')
with con:
    cur = con.cursor()
    for table in ['goals', 'natres', 'pubtrans', 'lifequality', 'housing', 'recreation']:
        sql = create_table(table, *generate_pairs('_', *getattr(globals()['definitions'], table)))
        print sql
        cur.execute(sql)

    sql2 = """CREATE TABLE persinfo (
       id INTEGER NOT NULL PRIMARY KEY,
       remote_addr VARCHAR(255),
       timestamp DATETIME,
       session_id VARCHAR(255),
       sex VARCHAR(255),
       yearofbirth VARCHAR(255),
       formerexperience VARCHAR(255),
       reference VARCHAR(255),
       profession VARCHAR(255),
       difficulty VARCHAR(255)
      );"""
    print sql2
    cur.execute(sql2)

print "done."
