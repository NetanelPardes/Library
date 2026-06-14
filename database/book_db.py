import mysql.connector
from fastapi import HTTPException
from database.db_connection import get_connection

optional_genre =  ['Fiction' , 'Non-Fiction' , 'Science' , 'History' , 'Other']

class Book:
    def __init__(self):
        pass
    
    def create_book(self,data):
        if data['genre'] in optional_genre:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO books (title , author , genre , is_available) VALUES (%s, %s, %s, %s)" ,(data['title'],data['author'], data['genre'],True))
            
            conn.commit()
            
            new_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return new_id
        
        raise HTTPException(status_code=404, detail="The book definition is incorrect.")
            

    def get_all_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books")

        all_books = cursor.fetchall()

        cursor.close()
        conn.close()

        return all_books

    def get_book_by_id(self,id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books WHERE id = %s" , (id,))

        book = cursor.fetchall()

        cursor.close()
        conn.close()

        return book

    def update_book(self,id, data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        set_parts = [f"{key} = %s" for key in data.keys()]
        set_cluse = " ,".join(set_parts)
        sql = f"UPDATE books set {set_cluse} WHERE id = %s"
        val = list(data.values()) + [id]
        cursor.execute(sql,val)

        conn.commit()

        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed

    def set_available(self,id, val, member_id):
        pass

    def count_total_books(self):
        pass

    def count_available_books(self):
        pass

    def count_borrowed_books(self):
        pass

    def count_by_genre(self,genre):
        pass

    def count_active_borrows_by_member(self,member_id):
        pass

    def book_available(self,id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books WHERE id = %s AND is_available = %s" , (id,1))

        book = cursor.fetchall()

        cursor.close()
        conn.close()

        return book