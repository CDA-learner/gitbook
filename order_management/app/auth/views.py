#!coding:utf-8
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User,Role,Order
from ..cjsonencoder import CJsonEncoder
from .forms import LoginForm, RegistrationForm
import json


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data) and user.status==u"启用":
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash(u'无效的账号或密码.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth.route('/addUser', methods=['GET', 'POST'])
def addUser():
    if request.method=="POST":
        username=request.form.get("username",None)
        password=request.form.get("password",None)
        roletype=request.form.get("roletype",None)
        role=Role.query.filter_by(name=roletype).first()
        department=request.form.get('department',None)
        founder=request.form.get('founder',None)
        notes=request.form.get('notes',None)
        status=request.form.get('status',None)
        user=User.query.filter_by(username=username).first()
        if user:
            return json.dumps(u"该账号已注册!")
        user=User(username=username,
                  password=password,
                  role=role,
                  department=department,
                  founder=founder,
                  notes=notes,
                  status=status
                  )
        db.session.add(user)
        db.session.commit()
        return json.dumps(u"注册账号成功!")

@auth.route('/editorUser', methods=['GET', 'POST'])
def editorUser():
    if request.method=="POST":
        id=request.form.get("editorId",None)
        username=request.form.get("username",None)
        password=request.form.get("password",None)
        roletype=request.form.get("roletype",None)
        role=Role.query.filter_by(name=roletype).first()
        department=request.form.get('department',None)
        founder=request.form.get('founder',None)
        notes=request.form.get('notes','')
        status=request.form.get('status',None)
        user_id=User.query.filter_by(id=id).first()
        user_username=User.query.filter_by(username=username).first()
        if user_username and user_username != user_id:
            print("该账号已注册")
            return json.dumps(u"该账号已注册!")
        user_id.username=username
        user_id.password=password
        user_id.role=role
        user_id.department=department
        user_id.notes=notes
        user_id.status=status
        db.session.add(user_id)
        db.session.commit()
        print("编辑用户成功")
        return json.dumps(u"编辑用户成功!")


        
@auth.route('/delUser', methods=['GET', 'POST'])
def delUser():
    if request.method=="POST":
        id=json.loads(request.form.get("id",None))
        user=User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return json.dumps(u"删除账号成功!")
        
@auth.route('/delUsers', methods=['GET', 'POST'])
def delUsers():
    if request.method=="POST":
        ids=json.loads(request.form.get("ids",None))
        for id in ids:
            user=User.query.filter_by(id=id).first()
            db.session.delete(user)
        db.session.commit()
        return json.dumps(u"删除账号成功!")

@auth.route('/userStatus', methods=['GET', 'POST'])
def userStatus():
    if request.method=="POST":
        id=json.loads(request.form.get("id",None))
        user=User.query.filter_by(id=id).first()
        if user.status==u"启用":
            user.status=u"禁用"
        else:
            user.status=u"启用"
        db.session.add(user)
        db.session.commit()
        return json.dumps("登录状态改变成功！")

@auth.route('/userlist', methods=['GET', 'POST'])
@login_required
def userList():
    roles=Role.query.all()
    users=User.query.all()
    current_role={"username":current_user.username,"role":current_user.role.name}
    js_users=[]
    for i in users:
        userDict={
            'id':i.id,
            'username':i.username,
            'role':i.role.name,
            'department':i.department,
            'founder':i.founder,
            'notes':i.notes.replace("\r\n","<br>"),
            'status':i.status
            }
        js_users.append(userDict)
    return render_template("userslisttest.html",
                            users=users,
                            roles=roles,
                            current_role=json.dumps(current_role),
                            js_users=json.dumps(js_users),
                           )




