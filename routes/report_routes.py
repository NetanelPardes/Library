from fastapi import APIRouter,Query
from database.book_db import Book
from database.member_db import Member

router = APIRouter()

my_book = Book()
my_member = Member()

@router.get("/reports/summary")
def count_not_available_books():
    return {"not available books" : my_book.count_borrowed_books()}

@router.get("/reports/books-by-genre")
def count_by_genre(genre:str = Query(default=None)):
    if genre:
        return {"books" : my_book.count_by_genre(genre)}
    return {"genres" : my_book.count_of_genres()}