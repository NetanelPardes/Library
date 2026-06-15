from fastapi import APIRouter,HTTPException
from database.book_db import Book
from database.member_db import Member
import logging
from logs.log_config import logger

logger = logging.getLogger(__name__)

router = APIRouter()

my_book = Book()
my_member = Member()

@router.post("/books")
def new_book(new_book:dict):
    """
    Handles creating a new book.
    """
    logger.info("A request for a new book has been received.")
    logger.info("New book created successfully")
    return {"book created with id" :my_book.create_book(new_book)}

@router.get("/books")
def show_all_books():
    """
    Handles returning all books.
    """
    logger.info("A request to display all books has been received.")
    logger.info("All books are displayed successfully.")
    return {"books" : my_book.get_all_books()}

@router.get("/books/{id}")
def get_book_by_id(id:int):
    """
    Handles returning a book by ID.
    """
    logger.info("A request has been received to display a book by id.")
    book = my_book.get_book_by_id(id)
    if not book:
        logger.error("This id %s does not exist in the system.",id)
        raise HTTPException(status_code=404,detail="There is no such book id.")
    logger.info("The book %d was successfully submitted." ,id)
    return{"book" :book}

@router.put("/books/{id}")
def update_book(id:int, new_data:dict):
    """
    Handles updating a book by ID.
    """
    logger.info("A request to update a book has been received.")
    update = my_book.update_book(id, new_data)
    if not update:
        logger.error("This id %s does not exist in the system.",id)
        raise HTTPException(status_code=404,detail="There is no such book id.")
    logger.info("Book %s updated successfully" ,id)
    return {"Book updated" : id}

@router.put("/books/{id}/borrow/{member_id}",status_code=200)
def borrow_book(id:int, member_id:int):
    """
    Handles borrowing a book for a member.
    """
    logger.info("A request to lend a book to a member has been received.")
    book = my_book.get_book_by_id(id)
    if book:
        if my_member.get_member_by_id(member_id):
            if my_member.is_member_active(member_id):
                if my_book.count_active_borrows_by_member(member_id) < 3:
                    if book["is_available"]:     
                        my_book.set_available(id,True,member_id)
                        logger.info("The book %s was loaned to member %s.",id ,member_id)
                        return {
                            "message": "Book borrowed successfully",
                            "book_id": id,
                            "member_id": member_id
                        }
                    else:
                       logger.error("The book %s is not available for borrowing." , id)
                       raise HTTPException(status_code=400, detail="Book is not available")
                else:
                    logger.error("The accumulator %s cannot lend another book",member_id)
                    raise HTTPException(status_code=400,detail="Member has reached maximum borrows")
            else:
                logger.error("Member %s is inactive." , member_id)
                raise HTTPException(status_code=400, detail="The member is inactive.")
        else:
            logger.error("The member %s does not exist." , member_id)
            raise HTTPException(status_code=404, detail="The friend does not exist.")
    else:
        logger.error("The book %s does not exist." ,id)
        raise HTTPException(status_code=404, detail="The book does not exist.")


@router.put("/books/{id}/return/{member_id}")
def return_book(id:int , member_id:int):
    """
    Handles returning a borrowed book from a member.
    """
    logger.info("A request to return a borrowed book has been received.")
    if my_book.get_book_by_id(id):
        if my_member.get_member_by_id(member_id):
            if my_book.book_borrow_to_member(id, member_id):
                my_book.set_available(id,False,member_id)
                logger.info("The book %s was returned from loan from month %s.",id ,member_id)
                return {
                    "message": "Book return successfully",
                    "book_id": id,
                    "member_id": member_id
                    }
            else:
                logger.error("The book %s is not on loan to member %s.",id ,member_id)
                raise HTTPException(status_code=400, detail="This book is not lent to a friend.")
        else:
            logger.error("The member %s does not exist." , member_id)
            raise HTTPException(status_code=404, detail="The friend does not exist.")
    else:
        logger.error("The book %s does not exist." ,id)
        raise HTTPException(status_code=404, detail="The book does not exist.")

