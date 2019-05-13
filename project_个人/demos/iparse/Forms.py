#! usr/bin/env python
# coding:utf-8

from flask import Flask
from flask_wtf import Form
from wtforms import FieldList,StringField
from wtforms.validators import DataRequired


class Myform(Form):
    user = StringField('username',validators=[DataRequired()])
