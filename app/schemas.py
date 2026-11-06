from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    category: Optional[str] = None
    total_copies: int = 1
    available_copies: int = 1


class BookResponse(BaseModel):
    book_id: int
    title: str
    author: str
    isbn: Optional[str] = None
    category: Optional[str] = None
    total_copies: int
    available_copies: int

    model_config = ConfigDict(from_attributes=True)

class MemberCreate(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None


class MemberResponse(BaseModel):
    member_id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    joined_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

class LoanCreate(BaseModel):
    book_id: int
    member_id: int
    due_date: date


class LoanResponse(BaseModel):
    loan_id: int
    book_id: int
    member_id: int
    borrow_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str

    model_config = ConfigDict(from_attributes=True)