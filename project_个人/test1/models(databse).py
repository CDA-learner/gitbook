from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    department = db.Column(db.String(64))
    founder = db.Column(db.String(64))
    notes = db.Column(db.Text)
    status = db.Column(db.String(64))
    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(64), index=True)
    malfunctionTime = db.Column(db.String(128))
    malfunctionDetail = db.Column(db.Text)
    recordCustomer = db.Column(db.String(64))
    malfunctionReason = db.Column(db.Text)
    processStatus = db.Column(db.String(64))
    restoreTime = db.Column(db.String(128))
    duration = db.Column(db.String(64))
    processPeople = db.Column(db.String(64))
    delstatus = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Order %r>' % self.department
    
@login_manager.user_loader
def load_user(user_id):

    if user_id is None:
        return redirect(url_for('auth.login'))
#   print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%s,%s,%s"%(current_user,current_user.is_active,current_user.is_authenticated) 
    return User.query.get(int(user_id))
