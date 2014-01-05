#!/usr/local/bin/python

from flask import Flask, abort, jsonify, render_template, request, url_for, g
import cv2
import numpy as np
import os
from pprint import pprint

app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
    g.root = '/labs/playground/cv/'
    
@app.after_request
def after_request(response):
    return response

@app.route('/')
def index():
    return 'entry point'

@app.route('/canny')
def canny():
    return render_template('canny.html')

@app.route('/cannyedge/<image>')
def cannyedgedetect(image=None):
    try:
        srcpath = os.path.join(app.root_path, '../images/')
        th1 = request.args.get('th1', type=int) or 50
        th2 = request.args.get('th2', type=int) or 100
        if th1 > 50 or th2 > 100:
            return 'Invalid Request'
        filename = image + '_edge_' + str(th1) + '_' + str(th2) + '.jpg'
        if os.access(srcpath + '/applied/' + filename, os.F_OK):
            issave = True
            #app.logger.debug(filename)
        else:
            src = cv2.imread(srcpath + image + '.jpg', 0)
            edge = cv2.canny(src, th1, th2)
            issave = cv2.imwrite(srcpath + '/applied/' + filename, edge)
        if issave:
            dstpath = g.root + '../images/applied/' + filename
            print dstpath
            content = dstpath
        else:
            content = 'Request Failed'
        return content
    except SystemError, e:
        return e.message

@app.route('/stardetector')
def stardetector():
    return render_template('stardetector.html')

@app.route('/starkeypoints/<image>')
@app.route('/starkeypoints/<image>/maxsize/<int:maxsize>')
@app.route('/starkeypoints/<image>/maxsize/<int:maxsize>/threshold/<int:threshold>/projected/<int:projected>/binarized/<int:binarized>/suppress/<int:suppress>')
def getstarkeypoints(image=None, maxsize=45, threshold=30, projected=10, binarized=8, suppress=5):
    path = os.path.join(app.root_path, "../images/")
    img = cv2.imread(path + image + '.jpg', 0)
    params = (maxsize, threshold, projected, binarized, suppress)
    storage = cv2.cv.CreateMemStorage()
    keypoints = cv2.cv.GetStarKeypoints(cv2.cv.fromarray(img), storage, params)
    datalist = []
    for keypoint in keypoints:
        data = {'x':keypoint[0][0],
                'y':keypoint[0][1],
                'size':keypoint[1],
                'response':keypoint[2]}
        datalist.append(data)
    return jsonify(name=image,
                   width=img.shape[0],
                   height=img.shape[1],
                   keypoints=datalist)

@app.errorhandler(404)
def notfound(error):
    return 'page not found', 404
