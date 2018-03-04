class User:
    '''
    This is a class that holds the methods of each user.
    retrieves it from the database and also stores the user's date into the databae.
    '''
    def __init__(self, bankid, username, password, name, designation):
        self.bankid = bankid
        self.username = username
        self.password = password
        self.name = name
        self.designation = designation
    def getbankid(self):
        return self.bankid
    def getusername(self):
        return self.username
    def getpassword(self):
        return self.password
    def getname(self):
        return self.name
    def getdesignation(self):
       return self.designation
    @classmethod
    def getuser(cls):
        return cls(bankid, username, password, name, designation)
