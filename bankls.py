from flask import Flask, render_template, request, redirect
from flask import url_for
from users import User
from  dbhelper import  DBHelper

DB = DBHelper()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/homepage',methods={'POST'})
def homepage():
    if request.form.get('login') == 'login':
        username = request.form.get('username')
        password = request.form.get('password')
        if DB.login(username, password):
          rows = DB.select_details(username)
          return render_template('homepage.html',username=username,rows=rows)
    if request.form.get('login') == 'register':
        bankid = request.form.get('bankid')
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('flname')
        designation = request.form.get('designation')
        DB.insert_user(bankid, username, password, name, designation)
        #rows = DB.select_details(username)
        return render_template('homepage.html',username=username)
    return redirect(url_for('home'))

if __name__ == '__main__':
    import os
    host = os.environ.get('IP','82.196.12.230')
    app.run(debug=True,host=host)
