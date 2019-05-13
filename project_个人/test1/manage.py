from flask import Flask
from flask import render_template
import

app = Flask(__name__,static_url_path='/static',static_folder='static',template_folder='templates')


@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route('/init_databse')
def init_databse():
    pass



if __name__ == '__main__':
    app.run()

    
#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Order
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Order=Order)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver',Server(host='127.0.0.1',port=8090))



if __name__ == '__main__':
    manager.run()