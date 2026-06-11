import mysql.connector

class Member:
    def __int__(self,name,email):
        self.name = name
        self.email = email
        self.is_active = True
        self.total_borrows = 0