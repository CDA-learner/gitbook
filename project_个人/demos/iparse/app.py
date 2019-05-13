from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from Forms import Myform
from flask_bootstrap import Bootstrap
import pymysql



app = Flask(__name__,static_url_path='',root_path='E:\project_个人\iparse')
bootstrap =Bootstrap(app)

@app.route('/')
def index():
    return render_template('sitelist.html')


# @app.route('/login', methods=('GET', 'POST'))
# def login():
#     # form = Myform()
    # if form.validate_on_submit():
    #     if form.data['user'] == 'admin':
    #         return 'Admin login successfully!'
    #     else:
    #         return 'Wrong user!'
    # return render_template('login.html', form=form)


# 站点list 从mysql中读取
@app.route('/sitelist')
def sitelist():
    conn = pymysql.connect(host='*.*.*.*', user='root', password='root', db='mydb', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM user"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('index.html',u=u)





if __name__ == '__main__':
    app.run(debug=True)
