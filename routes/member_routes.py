from fastapi import APIRouter,HTTPException
from database.member_db import Member
router = APIRouter()

my_member = Member()

@router.post("/members")
def new_member(new_member:dict):
    return {"member created with id" :my_member.create_member(new_member)}

@router.get("/members")
def show_all_members():
    return {"members" : my_member.get_all_members()}

@router.get("/members/{id}")
def get_member_by_id(id:int):
    member = my_member.get_member_by_id(id)
    if not member:
        raise HTTPException(status_code=404,detail="There is no such member id.")
    return{"member" :member}

@router.put("/members/{id}")
def update_member(id:int, new_data:dict):
    update = my_member.update_member(id, new_data)
    if not update:
        raise HTTPException(status_code=404,detail="There is no such member id.")
    return {"member updated" : id}

@router.put("/members/{id}/deactivate")
def deactivate_member(id:int):
    member = my_member.deactivate_member(id)
    if not member:
        raise HTTPException(status_code=404, detail="It doesn't work.")
    return {"member deactivate": id}

@router.put("/members/{id}/activate")
def activate_member(id:int ):
    member = my_member.activate_member(id)
    if not member:
        raise HTTPException(status_code=404, detail="It doesn't work.")
    return {"member activate": id}