from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Loan, Book, Member
from app.schemas import LoanCreate, LoanResponse

router = APIRouter(prefix="/loans", tags=["Loans"])


# GET ALL LOANS
@router.get("/", response_model=list[LoanResponse])
def get_loans(db: Session = Depends(get_db)):
    return db.scalars(select(Loan)).all()


# BORROW A BOOK
@router.post("/", response_model=LoanResponse, status_code=201)
def borrow_book(loan: LoanCreate, db: Session = Depends(get_db)):

    if loan.due_date < date.today():
        raise HTTPException(status_code=400, detail="Due date cannot be in the past")

    book = db.get(Book, loan.book_id)
    member = db.get(Member, loan.member_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")

    new_loan = Loan(
        book_id=loan.book_id,
        member_id=loan.member_id,
        due_date=loan.due_date,
        borrow_date=date.today(),
        status="borrowed"
    )

    try:
        book.available_copies -= 1

        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)

    except Exception:
        db.rollback()
        raise

    return new_loan


# RETURN A BOOK
@router.put("/{loan_id}/return")
def return_book(loan_id: int, db: Session = Depends(get_db)):

    loan = db.get(Loan, loan_id)

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.status == "returned":
        raise HTTPException(status_code=400, detail="Book already returned")

    book = db.get(Book, loan.book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    loan.status = "returned"
    loan.return_date = date.today()
    book.available_copies += 1

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {"message": "Book returned successfully"}


# GET ONE LOAN
@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):

    loan = db.get(Loan, loan_id)

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    return loan