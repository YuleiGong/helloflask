#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ylgongPw @ 2020-03-17 18:19:12
from __future__ import unicode_literals
from __future__ import absolute_import

from flask import Flask,request,redirect,url_for,abort,\
        make_response,jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name','Human')

    return '<h1>Hello, {}!<h1>'.format(name)

@app.route('/hi')
def hi():
    return redirect(url_for('hello'))

@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to {}!'.format((2020 - year))

@app.route('/404')
def not_found():
    abort(404)

@app.route('/colors/<any(blue,white,red):color>')
def three_color(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'

"""
@app.route('/foo')
def foo():
    response = make_response('Hello World!')
    response.minetype = 'text/plain'
    return response
"""

@app.route('/foo')
def foo():
    return jsonify(message='Error!'),500



@app.route('/note', defaults={'content_type': 'text'})
@app.route('/note/<content_type>')
def note(content_type):
    content_type = content_type.lower()
    if content_type == 'text':
        body = '''Note
to: Peter
from: Jane
heading: Reminder
body: Don't forget the party!
'''
        response = make_response(body)
        response.mimetype = 'text/plain'
    elif content_type == 'html':
        body = '''<!DOCTYPE html>
<html>
<head></head>
<body>
  <h1>Note</h1>
  <p>to: Peter</p>
  <p>from: Jane</p>
  <p>heading: Reminder</p>
  <p>body: <strong>Don't forget the party!</strong></p>
</body>
</html>
'''
        response = make_response(body)
        response.mimetype = 'text/html'
    elif content_type == 'xml':
        body = '''<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Peter</to>
  <from>Jane</from>
  <heading>Reminder</heading>
  <body>Don't forget the party!</body>
</note>
'''
        response = make_response(body)
        response.mimetype = 'application/xml'
    elif content_type == 'json':
        body = {"note": {
            "to": "Peter",
            "from": "Jane",
            "heading": "Remider",
            "body": "Don't forget the party!"
        }
        }
        response = jsonify(body)
        # equal to:
        # response = make_response(json.dumps(body))
        # response.mimetype = "application/json"
    else:
        abort(400)
    return response

@app.route("/set/<name>")
def set_cookie(name):
    response = make_response(redirect(url_for("hello")))
    response.set_cookie('name',name)
    return response

