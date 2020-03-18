#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ylgongPw @ 2020-03-17 18:19:12
from __future__ import unicode_literals
from __future__ import absolute_import


import os
from flask import Flask,request,redirect,url_for,abort,\
        make_response,jsonify,session,g
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY','secret string')


def is_sefe_url(target):
    print (request.host_url)
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url,target))

    return test_url.scheme in ('http','https') and \
            ref_url.netloc == test_url.netloc

def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'),request.referrer:
        if not target:
            continue
        if is_sefe_url(target):
            return redirect(target)

    return redirect(url_for(default,**kwargs))


@app.before_request
def get_name():
    g.name = request.args.get('name')


@app.route('/')
@app.route('/hello')
def hello():
    name = g.name
    if name is None:
        name = request.cookies.get('name','Human')
    response = '<h1>Hello, {}!<h1>'.format(name)
    if 'logged_in' in session:
        response += '[Authenticated]' #已经认证
    else:
        response += '[Not Authenticated]'

    return response



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

@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="{}">Do something</a>'\
            .format(url_for('do_something',next=request.full_path))

@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="{}">Do something</a>'\
            .format(url_for('do_something',next=request.full_path))



@app.route('/do_something')
def do_something():

    return redirect_back()


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

@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)

    return 'Welcome to admin page'


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')

    return redirect(url_for('hello'))

@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return """
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function() {
        $('#load').click(function() {
            $.ajax({
                url: '/more',
                type: 'get',
                success: function(data){
                    $('.body').append(data);
                }
            })
        })
    })
    </script>""" % post_body

@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)
