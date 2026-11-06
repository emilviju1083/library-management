from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


# GET ALL BOOKS
@router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.scalars(select(Book)).all()


# GET ONE BOOK
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


# ADD BOOK
@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):

    if book.total_copies < 0 or book.available_copies < 0:
        raise HTTPException(status_code=400, detail="Copies cannot be negative")

    if book.available_copies > book.total_copies:
        raise HTTPException(status_code=400, detail="Available copies cannot exceed total copies")

    new_book = Book(**book.model_dump())

    db.add(new_book)

    try:
        db.commit()
        db.refresh(new_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ISBN already exists")

    return new_book


# UPDATE BOOK
@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):

    book = db.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    data = updated_book.model_dump()

    if data["total_copies"] < 0 or data["available_copies"] < 0:
        raise HTTPException(status_code=400, detail="Copies cannot be negative")

    if data["available_copies"] > data["total_copies"]:
        raise HTTPException(status_code=400, detail="Available copies cannot exceed total copies")

    for key, value in data.items():
        setattr(book, key, value)

    try:
        db.commit()
        db.refresh(book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ISBN already exists")

    return book


# DELETE BOOK
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):

    book = db.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a book that has loan records"
        )

    return {"message": "Book deleted successfully"}