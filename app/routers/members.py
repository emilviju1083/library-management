from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Member
from app.schemas import MemberCreate, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])


# GET ALL MEMBERS
@router.get("/", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return db.scalars(select(Member)).all()


# GET ONE MEMBER
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):

    member = db.get(Member, member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


# ADD MEMBER
@router.post("/", response_model=MemberResponse, status_code=201)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):

    new_member = Member(**member.model_dump())

    db.add(new_member)

    try:
        db.commit()
        db.refresh(new_member)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")

    return new_member


# UPDATE MEMBER
@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, updated_member: MemberCreate, db: Session = Depends(get_db)):

    member = db.get(Member, member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    for key, value in updated_member.model_dump().items():
        setattr(member, key, value)

    try:
        db.commit()
        db.refresh(member)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")

    return member


# DELETE MEMBER
@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):

    member = db.get(Member, member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a member who has loan records"
        )

    return {"message": "Member deleted successfully"}