from flask import Flask, render_template, request, redirect
from flask import url_for
import pandas as pd
import pandas.io.sql as sql
from sklearn.ensemble import  RandomForestClassifier
import sqlite3
from features import features

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
        rows = [[0, bankid, username, password, name, designation ]] 
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
    details = {'name': request.form.get('name'), 
        'grade': request.form.get('grade'),
        'sub_grade': request.form.get('sub_grade'),
        'short_emp': int(request.form.get('short_emp')), 
        'emp_length_num': int(request.form.get('emp_length_num')),
        'home_ownership':request.form.get('home_ownership'), 
        'dti': float(request.form.get('dti')),
        'purpose':request.form.get('purpose'),
        'term':request.form.get('term'), 
        'last_delinq_none': int(request.form.get('last_delinq_none')),
        'last_major_derog_none': int(request.form.get('last_major_derog_none')), 
        'revol_util': float(request.form.get('revol_util')),
        'total_rec_late_fee': float(request.form.get('total_rec_late_fee')), 
        'staff_id': int(request.form.get('staff_id')),
        'safe_loans':0
    }
    custname = details['name']
    con = sqlite3.connect('bankls.db')
    cur = con.cursor()

    # getting data from the database
    data = sql.read_sql('select * from customer limit 5000',con)
    data = data.drop(['id','name','staff_id'],axis=1)

    # making a dataframe from the form received from customer.html
    df = pd.Series(details)
    df1 = df.to_frame().T
    newdf = df1.drop(['name','staff_id'],axis=1)
    newdf['dti'] = newdf['dti'].astype('float')
    newdf['safe_loans'] = newdf['safe_loans'].astype('int')
    newdf['emp_length_num'] = newdf['emp_length_num'].astype('int')
    newdf['short_emp'] = newdf['short_emp'].astype('int')
    newdf['last_delinq_none'] = newdf['last_delinq_none'].astype('int')
    newdf['last_major_derog_none'] = newdf['last_major_derog_none'].astype('int')
    newdf['revol_util'] = newdf['revol_util'].astype('float')
    newdf['total_rec_late_fee'] = newdf['total_rec_late_fee'].astype('float')

 

    data_df = data.append(newdf,ignore_index=True)

    # removing categorical variables for processing and 
    # turning these variables into objects for processing
    cats = []
    for c, d in zip(data_df.columns, data_df.dtypes):
       if d == 'object':
           cats.append(c)

    cats_data = data_df[cats]

    # doing 1 hot encoding on data
    hotencoding_database = pd.get_dummies(cats_data, prefix='feats_')

    # removing categorical data from dataframes
    sdata = data_df.drop(cats,axis=1)

    # joining them together
    alldata = hotencoding_database.join(sdata)
    # separating the data
    ddf = alldata.tail(1)
    alldata = alldata.drop(alldata.index[-1])

    target_data = alldata['safe_loans']
    feats_data = alldata.drop('safe_loans',axis=1)
    ddf = ddf.drop('safe_loans',axis=1)

    # performing actual classification and predictions
    # using random forest classifier
    classifier = RandomForestClassifier()
    rforest = classifier.fit(feats_data, target_data)

    # getting results for a yes or a no from the classifier
    safe_loan = rforest.predict(ddf)

    # saving data into database
    query = """
          insert into customer (name,grade,sub_grade,short_emp, 
          emp_length_num,home_ownership,
          dti,purpose,term,last_delinq_none,last_major_derog_none,
          revol_util,total_rec_late_fee,safe_loans,staff_id)
        values  (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    dd = [details['name'],details['grade'],details['sub_grade'],
      details['short_emp'],details['emp_length_num'],details['home_ownership'],
      details['dti'],details['purpose'],details['term'], 
      details['last_delinq_none'],details['last_major_derog_none'],
      details['revol_util'],details['total_rec_late_fee'],
      int(safe_loan),details['staff_id']
    ]
    cur.execute(query,dd)
    con.commit()
    con.close()
    return render_template('results.html', 
      custname = custname, safe_loan=safe_loan,
      staff_id=details['staff_id'])

if __name__ == '__main__':
    import os
    host = os.environ.get('IP','82.196.12.230')
    app.run(debug=True,host=host)
