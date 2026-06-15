import mysql.connector
from fastapi import HTTPException
from database.db_connection import DBconnection
from database.member_db import Member
from logs.log_config import logger
import logging

logger = logging.getLogger(__name__)
optional_genre =  ['Fiction' , 'Non-Fiction' , 'Science' , 'History' , 'Other']

class Book:
    def __init__(self):
        """
        Initializes the Book database handler.
        """
        self.db = DBconnection()
    
    def create_book(self,data):
        """
        Creates a new book in the books table.
        """
        if data['genre'] in optional_genre:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO books (title , author , genre , is_available) VALUES (%s, %s, %s, %s)" ,(data['title'],data['author'], data['genre'],True))
            
            conn.commit()
            
            new_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return new_id
        
        raise HTTPException(status_code=404, detail="The book definition is incorrect.")
            
    def get_all_books(self):
        """
        Returns all books from the books table.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books")

        all_books = cursor.fetchall()

        cursor.close()
        conn.close()

        return all_books

    def get_book_by_id(self,id):
        """
        Returns a single book by its ID.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books WHERE id = %s" , (id,))

        book = cursor.fetchone()

        cursor.close()
        conn.close()

        return book

    def update_book(self,id, data):
        """
        Updates the given fields of a book by its ID.
        """
        conn = self.db.get_connection()
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

    def set_available(self, id, val, member_id):
        """
        Updates a book availability status for borrow or return actions.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        if val == True:
            cursor.execute(
                "UPDATE books SET is_available = FALSE, borrowed_by_member_id = %s WHERE id = %s",
                (member_id, id)
            )
            conn.commit()
            Member.increment_borrows(member_id)
            changed = cursor.rowcount > 0

        else:
            cursor.execute(
                "UPDATE books SET is_available = TRUE, borrowed_by_member_id = NULL WHERE id = %s",
                (id,)
            )
            conn.commit()
            changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed

    def count_total_books(self):
        """
        Returns the total number of books in the database.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT count(*) as total FROM books")

        books = cursor.fetchone()

        cursor.close()
        conn.close()

        return books["total"]

    def count_available_books(self):
        """
        Returns the number of currently available books.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT count(*) as total FROM books WHERE is_available = TRUE")

        books = cursor.fetchone()

        cursor.close()
        conn.close()

        return books["total"]

    def count_borrowed_books(self):
        """
        Returns the number of currently borrowed books.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT count(*) as total FROM books WHERE is_available = FALSE")

        books = cursor.fetchone()

        cursor.close()
        conn.close()

        return books["total"]

    def count_by_genre(self,genre):
        """
        Returns the number of books for a specific genre.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT genre ,count(*) as total FROM books WHERE genre = %s GROUP BY genre" ,(genre,))

        member = cursor.fetchall()

        cursor.close()
        conn.close()

        return member

    def count_of_genres(self):
        """
        Returns the number of books grouped by genre.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT genre ,count(*) as total FROM books GROUP BY genre")

        member = cursor.fetchall()

        cursor.close()
        conn.close()

        return member

    def count_active_borrows_by_member(self, member_id):
        """
        Returns how many books the member is currently borrowing.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM books
            WHERE borrowed_by_member_id = %s
        """, (member_id,))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result["total"]
        
    def book_borrow_to_member(self,id, member_id):
        """
        Checks if a specific book is borrowed by a specific member.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books WHERE id = %s AND borrowed_by_member_id = %s" , (id,member_id))

        member = cursor.fetchone()

        cursor.close()
        conn.close()

        return member