import csv
import sqlite3

fp = open('mini_loan_data.csv')
con = sqlite3.connect('bankls.db')

query = """
  insert into customer (grade,sub_grade,short_emp,emp_length_num,home_ownership, 
            dti,purpose,term,last_delinq_none,last_major_derog_none,revol_util,total_rec_late_fee,safe_loans)
   values  (?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

cur = con.cursor()
reader = csv.reader(fp)

i = 1
for row in reader:
    i += 1
    cur.execute(query, row[1:])
    if i % 100 == 0:
        con.commit()
con.commit()
con.close()
fp.close()
