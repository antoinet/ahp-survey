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

print "done."
