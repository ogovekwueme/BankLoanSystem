from flask import Flask, render_template, request, redirect
from flask import url_for
import numpy as np
import pandas as pd
from sklearn.ensemble import  RandomForestClassifier
import sqlite3

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
        try:
            cursor = con.cursor()
            cursor.execute("select * from staff where username='"+username+"'")
        except:
            print 'Error logging in'
        else:
            rows = cursor.fetchall()
            for row in rows:
                if username == row[2] and password == row[3]:
                    cn = True
    if request.form.get('login') == 'register':
        bankid = int(request.form.get('bankid'))
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('flname')
        designation = request.form.get('designation')
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

@app.route('/customer/<username>/')
def customer(username):
    con =sqlite3.connect('bankls.db')
    cur = con.cursor()
    cur.execute("select id from staff where username='"+username+"'")
    rows = cur.fetchall()
    for row in rows:
        staffid = row[0]
    return render_template('customer.html',staffid=staffid)

@app.route('/<staff_id>/results',methods={'post'})
def results(staff_id):
    details = {'name': equest.form.get('name'), 
        'grade':request.form.get('grade'),
        'sub_grade':request.form.get('sub_grade'),
        'short_emp,':request.form.get('short_emp'), 
        'emp_length_num':request.form.get('emp_length_num'),
        'home_ownership':request.form.get('home_ownership'), 
        'dti':request.form.get('dti'),
        'purpose':request.form.get('purpose'),
        'term':request.form.get('term'), 
        'last_delinq_none':request.form.get('last_term_delinq_none'),
        'last_major_derog_none':request.form.get('last_major_derog_none'), 
        'revol_util':request.form.get('revol_tuil'),
        'total_rec_late_fee':request.form.get('total_rec_late_fee'), 
        'staff_id':request.form.get('staff_id')
    }

    
    return render_template('results.html', custname = custname)

if __name__ == '__main__':
    import os
    host = os.environ.get('IP','82.196.12.230')
    app.run(debug=True,host=host)
