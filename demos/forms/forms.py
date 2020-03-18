#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ylgongPw @ 2020-03-18 17:29:10
from __future__ import unicode_literals
from __future__ import absolute_import

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField("Log in")

