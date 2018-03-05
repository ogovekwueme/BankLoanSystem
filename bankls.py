from flask import Flask, render_template, request, redirect
from flask import url_for
from users import User
from  dbhelper import  DBHelper
import sqlite3
DB = sqlite3.connect('bankls.db') #DBHelper()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/homepage',methods={'POST'})
def homepage():
    cn = False
    con = sqlite3.connect('bankls.db')
    if request.form.get('login') == 'login':
        username = request.form.get('username')
        password = request.form.get('password')
        #if DB.login(username, password):
        try:
            cursor = con.cursor()
            cursor.execute("select * from staff where username='"+username+"'")
        except:
            print 'Error logging in'
        else:
            rows = cursor.fetchall()
            for row in rows:
                if username == row[2] and password == row[3]:
                    #rows = DB.select_details(username)
                    cn = True
    if request.form.get('login') == 'register':
        bankid = int(request.form.get('bankid'))
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('flname')
        designation = request.form.get('designation')
        #DB.insert_user(bankid, username, password, name, designation)
        rows = [[bankid, username, password, name, designation ]] #DB.select_details(username)
        query = '''
            insert into staff (bankid, username, password, name, designation)
            values (?,?,?,?,?)
        '''
        try:
            cur = con.cursor()
            cur.execute(query, (bankid,username, password, name, designation))
            cn = True
        except:
            print 'Error processing query'
        else:
            con.commit()


    con.close()
    if cn:
        return render_template('homepage.html',username=username, rows=rows)

    return redirect(url_for('home'))

@app.route('/customer')
def customer():
    return render_template('customer.html')


if __name__ == '__main__':
    import os
    host = os.environ.get('IP','82.196.12.230')
    app.run(debug=True,host=host)
