#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, g, request, render_template
import json
import os
import re
import sqlite3
import time
from pprint import pprint

app = Flask(__name__)
app.config.update(
    #DATABASE = 'db/samples.db',
    DATABASE = 'db/catcafe.db',
    DEBUG = True
)

db = None
samples = None

def getdb():
    global db
    if db is None:
        db = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db
        
def querydb(query, args=(), one=False):
    cur = getdb().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def getsamples(update=False):
    global samples
    if update or samples is None:
        sql = 'SELECT id, filepath FROM samples'
        samples = querydb(sql)
    return samples

def getpos():
    sql = 'SELECT pos FROM progress'
    pos = querydb(sql, one=True)['pos']
    return pos

def updatepos(pos):
    sql = 'UPDATE progress SET pos=?'
    db = getdb()
    db.execute(sql, (pos,))
    db.commit()

def getstatus(pos):
    sql = 'SELECT status FROM samples WHERE id=?'
    row = querydb(sql, (pos + 1,), one=True)
    return (row['status'] if row else None)

def updatecoords(coords, pos):
    sql = 'UPDATE samples SET x=?, y=?, width=?, height=?, status=?, updated_date=? WHERE id=?'
    db = getdb()
    db.execute(sql, (coords['x'], coords['y'], coords['w'], coords['h'], 200, time.strftime('%Y-%m-%d %H:%M:%S'), pos))
    db.commit()

@app.route('/clipper')
def index():
    message = 'ready to load images ok.'
    samples = getsamples()
    imgtotal = len(samples)
    pos = getpos()
    if pos == imgtotal:
        message = 'complete !'
        return render_template('index.html', progress=100, message=message)
        
    try:
        imgsrc = samples[pos]['filepath']
    except IndexError as e:
        imgsrc = None

    status = getstatus(pos)
    remain = imgtotal - pos
    progress = 1.0*pos/imgtotal*100
    return render_template('index.html', imgsrc=imgsrc, imgtotal=imgtotal, pos=pos, status=status, remain=remain, progress=progress, message=message)
    
@app.route('/clipper/next')
def next():
    coords = json.loads(request.args.get('coords'))
    isskip = request.args.get('skip')
    samples = getsamples()
    pos = getpos()
    imgtotal = len(samples)
    app.logger.debug(coords)

    if coords is not None:
        updatecoords(coords, pos + 1)
        
    if pos < imgtotal:
        pos += 1
        updatepos(pos)
        
    try:
        imgsrc = samples[pos]['filepath']
    except IndexError as e:
        imgsrc = None

    status = getstatus(pos)    
    remain = imgtotal - pos
    progress = 1.0*pos/imgtotal*100
    return jsonify(imgsrc=imgsrc, pos=pos, status=status, remain=remain, progress=progress)

@app.route('/clipper/prev')
def prev():
    coords = json.loads(request.args.get('coords'))
    samples = getsamples()
    pos = getpos()
    imgtotal = len(samples)
    if pos > 0:
        pos -= 1
        updatepos(pos)
        
    try:
        imgsrc = samples[pos]['filepath']
    except IndexError as e:
        imgsrc = None

    status = getstatus(pos)
    remain = imgtotal - pos
    progress = 1.0*pos/imgtotal*100
    return jsonify(imgsrc=imgsrc, pos=pos, status=status, remain=remain, progress=progress)

@app.route('/clipper/progress', methods=['POST'])
def updateprogress():
    pos = json.loads(request.form['pos'])
    app.logger.debug(pos)
    if pos is not None:
        updatepos(pos)
        
    return jsonify(status=200, message='ok')

@app.route('/clipper/sync', methods=['POST'])
def syncdatabase():
    getsamples(update=True)
    return jsonify(status=200, message='ok')

## main
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
