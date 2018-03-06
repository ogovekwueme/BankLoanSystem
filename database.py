import sqlite3

try:
    con = sqlite3.connect('bankls.db')
except:
    import sys
    print 'Cannot Open databas'
    sys.exit()
else:
    sql = '''
        create table if not exists staff (
          id integer primary KEY autoincrement,
          bankid integer unique,
          username varchar(255),
          password varchar(255),
          name varchar(255),
          designation varchar(255)
        )
    '''
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

    sql1 = '''
        create table if not exists customer (
          id integer primary KEY autoincrement,
          name varchar(255),
        grade iteger,
        sub_grade varchar(2),
        short_emp integer,
        emp_length_num integer,
        home_ownership varchar(4),
        dti real,
        purpose varchar(60),
        term varchar(15),
        last_delinq_none integer,
        last_major_derog_none integer,
        revol_util real,
        total_rec_late_fee real,
        safe_loans integer,
        staff_id integer,
        foreign key (staff_id) references staff(id)
      )
    '''

    cur.execute(sql1)
    con.commit()
finally:
    if con:
        con.close()

