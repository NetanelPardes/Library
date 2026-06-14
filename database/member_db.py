import mysql.connector
from fastapi import HTTPException
from database.db_connection import DBconnection

class Member:
    def __init__(self,name =None,email=None):
        self.name = name
        self.email = email
        self.is_active = True
        self.total_borrows = 0
        self.db = DBconnection()

    def create_member(self,data):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO members (name , email , is_active , total_borrows) VALUES (%s, %s, %s, %s)" ,(data['name'],data['email'], True,0))
            
        conn.commit()
            
        new_id = cursor.lastrowid
            
        cursor.close()
        conn.close()
            
        return new_id

    def get_all_members(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members")

        all_members = cursor.fetchall()

        cursor.close()
        conn.close()

        return all_members
    
    def get_member_by_id(self,id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members WHERE id = %s" , (id,))

        member = cursor.fetchone()

        cursor.close()
        conn.close()

        return member
    
    def update_member(self,id, data):
        conn = self.db.get_connection()
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
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE members set is_active = FALSE WHERE id = %s",(id,))
        conn.commit()
        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed
    
    def activate_member(self,id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE members set is_active = TRUE WHERE id = %s",(id,))
        conn.commit()
        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed
    
    def increment_borrows(self,id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE members set total_borrows = total_borrows + 1 WHERE id = %s",(id,))
        conn.commit()
        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed
      
    def count_active_members(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT count(*) AS total FROM members WHERE is_active = TRUE")

        member = cursor.fetchone()

        cursor.close()
        conn.close()

        return member["total"]
    
    def get_top_member(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members ORDER BY total_borrows DESC")

        member = cursor.fetchall()

        cursor.close()
        conn.close()

        return member[0]
    
    def is_active(self,id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM members WHERE id = %s AND is_active = %s" , (id,1))


        member = cursor.fetchone()

        cursor.close()
        conn.close()

        return member
    
    def can_borrow(self,member_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) as total FROM books WHERE borrowed_by_member_id = %s HAVING tatal < 4" , (member_id,))

        member = cursor.fetchall()

        cursor.close()
        conn.close()

        return member
    