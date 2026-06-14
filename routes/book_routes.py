from fastapi import APIRouter,HTTPException
from database.book_db import Book

router = APIRouter()

my_book = Book()

@router.post("/books")
def new_book(new_book:dict):
    return {"book created with id" :my_book.create_book(new_book)}

@router.get("/books")
def show_all_books():
    return {"books" : my_book.get_all_books()}

@router.get("/books/{id}")
def get_book_by_id(id:int):
    book = my_book.get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=404,detail="There is no such book id.")
    return{"book" :book}

