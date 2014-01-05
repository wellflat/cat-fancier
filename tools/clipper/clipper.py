#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, g, request, render_template
import json
import os
import re
import sqlite3

app = Flask(__name__)
app.config.update(
    DATABASE = 'samples.db',
    POSITIVESAMPLES = 'positive.dat',
    NEGATIVESAMPLES = 'negative.dat',
    DEBUG = True,
    SECRET_KEY = 'chocolat',
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

def getsamples():
    global samples
    if samples is None:
        sql = 'SELECT id, filepath FROM samples WHERE status=100'
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

def updatecoords(coords):
    sql = 'UPDATE samples SET x=?, y=?, width=?, height=? WHERE id=?'
    db = getdb()
    db.execute(sql, (coords['x'], coords['y'], coords['width'], coords['height']))
    db.commit()

@app.before_request
def before():
    pass
    # g.positivefile = open(app.config['POSITIVESAMPLES'], 'a')
    # g.negativefile = open(app.config['NEGATIVESAMPLES'], 'a')

@app.route('/clipper')
def index():
    message = 'ready to load images ok.'
    samples = getsamples()
    imgtotal = len(samples)
    pos = getpos()
    if not imgtotal:
        message = 'error, image file not found'
    #counter = ''.join([str(pos+1).zfill(len(str(imgtotal))), ' of ', str(imgtotal)])
    try:
        imgsrc = samples[pos]['filepath']
    except IndexError as e:
        imgsrc = None
    remain = imgtotal - pos
    progress = 1.0*pos/imgtotal*100
    app.logger.debug(pos/imgtotal)
    return render_template('index.html', message=message, imgsrc=imgsrc, imgtotal=imgtotal, pos=pos, remain=remain, progress=progress)
    
@app.route('/clipper/next')
def next():
    isskip = request.args.get('skip')
    samples = getsamples()
    pos = getpos()
    imgtotal = len(samples)
    if pos < imgtotal:
        pos += 1
        updatepos(pos)
    try:
        imgsrc = samples[pos]['filepath']
    except IndexError as e:
        imgsrc = None
    remain = imgtotal - pos
    progress = 1.0*pos/imgtotal*100
    return jsonify(imgsrc=imgsrc, pos=pos, remain=remain, progress=progress)

@app.route('/clipper/previous')
def previous():
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
    remain = imgtotal - pos
    progress = 1.0*pos/imgtotal*100
    return jsonify(imgsrc=imgsrc, pos=pos, remain=remain, progress=progress)

## main
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
