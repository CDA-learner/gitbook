#!coding:utf-8
from flask import render_template, session,request, redirect, url_for, current_app
from flask_login import login_required, current_user
from .. import db
from ..models import User,Role,Order
from ..cjsonencoder import CJsonEncoder
from . import main
from .forms import NameForm
import json
import datetime 


            
@main.route('/', methods=['GET', 'POST'])
@login_required
def index0():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            return "OK"
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index0'))
    return render_template('index0.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

@main.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('bases.html')
    

@main.route('/orderlist', methods=['GET', 'POST'])
@login_required
def index():
    roles=Role.query.all()
    orders=Order.query.filter_by(delstatus=1).all()
    delorders=Order.query.filter_by(delstatus=0).all()
    current_role={"username":current_user.username,"role":current_user.role.name}
    js_orders=[]
    del_js_orders=[]
    for i in orders:
        orderDict={
            'id':i.id,
            'department':i.department,
            'malfunctionTime':i.malfunctionTime,
            'recordCustomer':i.recordCustomer,
            'processStatus':i.processStatus,
            'restoreTime':i.restoreTime,
            'processPeople':i.processPeople,
            'malfunctionDetail':i.malfunctionDetail.replace("\r\n","<br>"),
            'malfunctionReason':i.malfunctionReason.replace("\r\n","<br>"),
            'duration':i.duration
            }
        js_orders.append(orderDict)
    for i in delorders:
        orderDict={
            'id':i.id,
            'department':i.department,
            'malfunctionTime':i.malfunctionTime,
            'recordCustomer':i.recordCustomer,
            'processStatus':i.processStatus,
            'restoreTime':i.restoreTime,
            'processPeople':i.processPeople,
            'malfunctionDetail':i.malfunctionDetail.replace("\r\n","<br>"),
            'malfunctionReason':i.malfunctionReason.replace("\r\n","<br>"),
            'duration':i.duration
            }
        del_js_orders.append(orderDict)
    return render_template("orderlisttest.html",
                            orders=orders,
                            roles=roles,
                            current_role=json.dumps(current_role),
                            js_orders=json.dumps(js_orders),
                            del_js_orders=json.dumps(del_js_orders)
                           )




@main.route('/addOrder',methods=['GET','POST'])
@login_required
def addOrder():
    if request.method=="POST":
        department = request.form.get("department",None)
        malfunctionTime = request.form.get("malfunctionTime",None)
        malfunctionDetail = request.form.get("malfunctionDetail",None)
        recordCustomer = request.form.get("founder",None)
        if current_user.role.name==u"管理员":
            malfunctionReason=request.form.get("malfunctionReason",None)
            processStatus=request.form.get("processStatus",None)
            restoreTime=request.form.get("restoreTime",None)
            duration=request.form.get("duration",None)
            processPeople=request.form.get("processPeople",None)
            order=Order(department=department,
                    malfunctionTime=malfunctionTime,
                    malfunctionDetail=malfunctionDetail,
                    recordCustomer=recordCustomer,
                    malfunctionReason=malfunctionReason,
                    processStatus=processStatus,
                    restoreTime=restoreTime,
                    duration=duration,
                    processPeople=processPeople
                    )
        else:
            order=Order(department=department,
                    malfunctionTime=malfunctionTime,
                    malfunctionDetail=malfunctionDetail,
                    recordCustomer=recordCustomer,
                    malfunctionReason=u'',
                    processStatus=u'',
                    restoreTime=u'',
                    duration=u'',
                    processPeople=u''
                    )
        try:
            db.session.add(order)
            db.session.commit()
            print("正常执行")
        except: 
            print("异常输出")
        return json.dumps(u'添加记录成功!')
        
@main.route('/delOrder',methods=['GET','POST'])
@login_required
def delOrder():
    if request.method=="POST":
        id=json.loads(request.form.get("id",None))
        order=Order.query.filter_by(id=id).first()
        order.delstatus=0
        db.session.add(order)
        db.session.commit()
        return json.dumps(u"删除成功!")
    
@main.route('/delOrders',methods=['GET','POST'])
@login_required
def delOrders():
    if request.method=="POST":
        ids=json.loads(request.form.get("ids",None))
        for id in ids:
            order=Order.query.filter_by(id=id).first()
            order.delstatus=0
            db.session.add(order)
        db.session.commit()
        return json.dumps(u"工单批量删除成功!")
    
    

@main.route('/editorOrder',methods=['GET','POST'])
@login_required
def editorOrder():
    if request.method=="POST":
        id = request.form.get("editorId",None)
        order=Order.query.filter_by(id=id).first()
        if current_user.role.name==u"管理员":
            print('角色管理员')
            department = request.form.get("department",None)
            malfunctionTime = request.form.get("malfunctionTime",None)
            malfunctionDetail = request.form.get("malfunctionDetail",None)
            recordCustomer = request.form.get("founder",None)
            malfunctionReason=request.form.get("malfunctionReason",None)
            processStatus=request.form.get("processStatus",None)
            restoreTime=request.form.get("restoreTime",None)
            duration=request.form.get("duration",None)
            processPeople=request.form.get("processPeople",None)
            
            order.department=department
            order.malfunctionTime=malfunctionTime
            order.malfunctionDetail=malfunctionDetail
            order.recordCustomer=recordCustomer
            order.malfunctionReason=malfunctionReason
            order.processStatus=processStatus
            order.restoreTime=restoreTime
            order.duration=duration
            order.processPeople=processPeople
        elif current_user.role.name==u"客服主管" or current_user.role.name==u"客服值班":
            print("角色客服",order.malfunctionTime)
            department = request.form.get("department",None)
            malfunctionTime = request.form.get("malfunctionTime",None)
            malfunctionDetail = request.form.get("malfunctionDetail",None)
            recordCustomer = request.form.get("founder",None)
            
            order.department=department
            order.malfunctionTime=malfunctionTime
            order.malfunctionDetail=malfunctionDetail
            order.recordCustomer=recordCustomer
        else:
            print("角色运维值班")
            malfunctionReason=request.form.get("malfunctionReason",None)
            processStatus=request.form.get("processStatus",None)
            restoreTime=request.form.get("restoreTime",None)
            duration=request.form.get("duration",None)
            processPeople=request.form.get("processPeople",None)
            order.malfunctionReason=malfunctionReason
            order.processStatus=processStatus
            order.restoreTime=restoreTime
            order.duration=duration
            order.processPeople=processPeople
        try:
            db.session.add(order)
            db.session.commit()
            print("正常执行")
        except: 
            print("异常输出")
        return json.dumps(u'修改工单记录成功!')
    
    
    
    
    
    
    
    
    
    
    
