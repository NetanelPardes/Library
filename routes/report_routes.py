from fastapi import APIRouter,Query
from database.book_db import Book
from database.member_db import Member

router = APIRouter()

my_book = Book()
my_member = Member()

@router.get("/reports/summary")
def get_summary():
    """
    Handles returning the library summary report.
    """
    return {"total_books" : my_book.count_total_books(),
            "available_books" : my_book.count_available_books(),
            "currently_borrowed": my_book.count_borrowed_books(),
            "active_members" : my_member.count_active_members()
            }

@router.get("/reports/books-by-genre")
def count_by_genre(genre:str = Query(default=None)):
    """
    Handles returning book counts by genre.
    """
    if genre:
        return {"books" : my_book.count_by_genre(genre)}
    return {"genres" : my_book.count_of_genres()}

@router.get("/reports/top-member")
def get_top_member():
    """
    Handles returning the member with the highest borrow count.
    """
    return {"top_member": my_member.get_top_member()}

