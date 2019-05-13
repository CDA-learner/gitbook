#! usr/bin/env python
# coding:utf-8

from flask import Flask,render_template
from wtforms import Form
from Forms import Myform

app =Flask(__name__)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = Myform()
    if form.validate_on_submit():
        # if form.user.data == 'admin':
        if form.data['user'] == 'admin':
            return 'Admin login successfully!'
        else:
            return 'Wrong user!'
    return render_template('login.html', form=form)
