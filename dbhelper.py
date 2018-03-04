import sqlite3

class DBHelper:
    '''
    A class to retrieve and insert data into the database
    '''
    def connect(self, database='bankls.db'):
        return sqlite3.connect(database)
    def insert_user(self,bankid, username, password, name, designation):
        query = """
          insert into staff (bankid, username, password, name,
          designation) values (%s, %s, %s, %s, %s)
        """
        con = self.connect()
        try:
            with con.cursor() as cur:
                cur.execute(query % (bankid, username, password, name, designation))
            con.commit()
        except:
            print 'Trouble Connecting'
        finally:
            con.close()

    def login(self, username, password):
        query = 'select username,password from staff'
        con = self.connect()
        try:
            with  scon.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
            for row in rows:
               if username == row[0] and password == row[1]:
                   return True
        except:
           print 'Cannot Connect to Database'
        finally:
           con.close()
        return False
    def select_details(self, username):
        query = "select bankid, username, name, designation from staff where username='"+username+"';"
        con = self.connect()
        try:
            with con.cursor as cur:
                cur.execute(query)
                return cur.fetchall()
        except:
            print 'Cannot Connect'
        finally:
            con.close()
        return []
    def insert_cust(self,*args):
        pass
