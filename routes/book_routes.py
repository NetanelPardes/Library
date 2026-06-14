from fastapi import APIRouter
from database.book_db import Book

router = APIRouter()

my_book = Book()

@router.post("/books")
def new_book(new_book:dict):
    return {"book created with id" :my_book.create_book(new_book)}

@router.get("/books")
def show_all_books():
    return {"books" : my_book.get_all_books()}