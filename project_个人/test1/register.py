#! usr/bin/env python
# coding:utf-8

from wtforms import Form,BooleanField,StringField,validators


class Registration(Form):
    user = StringField('username:',[validators.Length(min=4,max=10,message=u'用户名长度有问题')])
    passwd = StringField('password:',
                        [validators.Length(min=8,max=20,message=u'输入长度有问题'),
                         validators.Regexp(regex="^(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
                                           message='密码至少8位，包含字母，特殊字符和数字')])
    accept_rules = BooleanField('我同意此协议',[validators.InputRequired()])

