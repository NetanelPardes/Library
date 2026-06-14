import mysql.connector
from fastapi import HTTPException
from database.db_connection import get_connection

class Member:
    def __int__(self,name,email):
        self.name = name
        self.email = email
        self.is_active = True
        self.total_borrows = 0

    def create_member(self,data):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO members (name , email , is_active , total_borrows) VALUES (%s, %s, %s, %s)" ,(data['name'],data['email'], True,0))
            
        conn.commit()
            
        new_id = cursor.lastrowid
            
        cursor.close()
        conn.close()
            
        return new_id

    def get_all_members(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members")

        all_members = cursor.fetchall()

        cursor.close()
        conn.close()

        return all_members
    
    def get_member_by_id(self,id):
        pass
    
    def update_member(self,id, data):
        pass
    
    def deactivate_member(self,id):
        pass
    
    def activate_member(self,id):
        pass
    
    def increment_borrows(self,id):
        pass
      
    def count_active_members(self):
        pass
    
    def get_top_member(self):
        pass
    