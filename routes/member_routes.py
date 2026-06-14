from fastapi import APIRouter
from database.member_db import Member
router = APIRouter()

my_member = Member()

@router.post("/members")
def new_member(new_member:dict):
    return {"member created with id" :my_member.create_member(new_member)}

@router.get("/members")
def show_all_members():
    return {"members" : my_member.get_all_members()}