import mysql.connector

class Book:
    def __init__(self,title,author,genre):
        self.title = title
        self.author = author
        self.genre = genre
        self.is_available = True
        self.borrowed_by_member_id = NULL
    
    def create_book(self,data):
        pass

    def get_all_books(self):
        pass

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