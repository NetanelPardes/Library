from fastapi import APIRouter,HTTPException
from database.book_db import Book
from database.member_db import Member

router = APIRouter()

my_book = Book()
my_member = Member()

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

@router.put("/books/{id}")
def update_book(id:int, new_data:dict):
    update = my_book.update_book(id, new_data)
    if not update:
        raise HTTPException(status_code=404,detail="There is no such book id.")
    return {"Book updated" : id}

@router.put("/books/{id}/borrow/{member_id}")
def borrow_book(id:int, member_id:int):
    if my_book.get_book_by_id(id):
        if my_member.get_member_by_id(member_id):
            if my_member.is_active(member_id):
                if my_book.count_active_borrows_by_member(member_id):
                    try:
                        my_book.set_available(id,True,member_id)
                        return {
                            "message": "Book borrowed successfully",
                            "book_id": id,
                            "member_id": member_id
                        }
                    except:
                        raise HTTPException(status_code=404, detail="There is a problem.")
                else:
                    raise HTTPException(status_code=404, detail="The friend cannot borrow a book.")
            else:
                raise HTTPException(status_code=404, detail="The member is inactive.")
        else:
            raise HTTPException(status_code=404, detail="The friend does not exist.")
    else:
        raise HTTPException(status_code=404, detail="The book does not exist.")


@router.put("/books/{id}/return/{member_id}")
def return_book(id:int , member_id:int):
    if my_book.get_book_by_id(id):
        if my_member.get_member_by_id(member_id):
            if my_book.book_borrow_to_member(id, member_id):
                try:
                    my_book.set_available(id,False,member_id)
                    return {
                        "message": "Book return successfully",
                        "book_id": id,
                        "member_id": member_id
                        }
                except:
                    raise HTTPException(status_code=404, detail="There is a problem.")
            else:
                    raise HTTPException(status_code=404, detail="This book is not lent to a friend.")
        else:
            raise HTTPException(status_code=404, detail="The friend does not exist.")
    else:
        raise HTTPException(status_code=404, detail="The book does not exist.")

