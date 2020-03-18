#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ylgongPw @ 2020-03-18 17:39:02
from __future__ import unicode_literals
from __future__ import absolute_import

import os
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session

from forms.forms import LoginForm


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


@app.route('/basic')
def basic():
    form = LoginForm()
    return render_template('basic.html', form=form)

@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    form = LoginForm()
    return render_template('bootstrap.html', form=form)


