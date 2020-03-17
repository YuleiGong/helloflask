#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ylgongPw @ 2020-03-17 15:40:23
from __future__ import unicode_literals
from __future__ import absolute_import

from flask import Flask
import click

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Hello Flask!<h1>"


@app.route("/hi")
@app.route("/hello")
def say_hello():
    return "<h1>Hello Flask!<h1>"

@app.route("/greet/<name>")
@app.route("/greet",defaults={'name':'Programer'})
def greet(name):
    return "<h1>Hello {}!<h1>".format(name)

@app.cli.command()
def hello():
    click.echo("Hello, Human!")
