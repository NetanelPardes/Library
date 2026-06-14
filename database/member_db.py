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
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members WHERE id = %s" , (id,))

        member = cursor.fetchall()

        cursor.close()
        conn.close()

        return member
    
    def update_member(self,id, data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        set_parts = [f"{key} = %s" for key in data.keys()]
        set_cluse = " ,".join(set_parts)
        sql = f"UPDATE members set {set_cluse} WHERE id = %s"
        val = list(data.values()) + [id]
        cursor.execute(sql,val)

        conn.commit()

        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed
    
    def deactivate_member(self,id):
        pass
    
    def activate_member(self,id):
        pass
    
    def increment_borrows(id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE members set total_borrows = total_borrows + 1 WHERE id = %s",(id,))
        conn.commit()
        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed
      
    def count_active_members(self):
        pass
    
    def get_top_member(self):
        pass
    
    def is_active(self,id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members WHERE id = %s AND is_active = %s" , (id,1))


        member = cursor.fetchall()

        cursor.close()
        conn.close()

        return member
    
    def can_borrow(self,member_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) as total FROM books WHERE borrowed_by_member_id = %s HAVING tatal < 4" , (member_id,))

        member = cursor.fetchall()

        cursor.close()
        conn.close()

        return member