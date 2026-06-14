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
        pass

    def update_book(self,id, data):
        pass

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