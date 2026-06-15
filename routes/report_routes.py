from fastapi import APIRouter,Query
from database.book_db import Book
from database.member_db import Member
from logs.log_config import logger
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

my_book = Book()
my_member = Member()

@router.get("/reports/summary")
def get_summary():
    """
    Handles returning the library summary report.
    """
    logger.info("A request to display a summary report has been received.")
    logger.info("Summary report displayed successfully")
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
    logger.info("A request has been received to display the books by genre.")
    if genre:
        logger.info("The request is accompanied by the genre The genre were successfully displayed")
        return {"books" : my_book.count_by_genre(genre)}
    logger.info("The genres were successfully presented")
    return {"genres" : my_book.count_of_genres()}

@router.get("/reports/top-member")
def get_top_member():
    """
    Handles returning the member with the highest borrow count.
    """
    logger.info("A request to display the most active member has been received.")
    logger.info("The most active member was successfully introduced.")
    return {"top_member": my_member.get_top_member()}

