from fastapi import FastAPI

from app.routers import books
from app.routers import members
from app.routers import loans

app = FastAPI(
    title="Library Management API",
    description="REST API for managing books, members, and loans",
    version="1.0.0"
)

app.include_router(books.router)
app.include_router(members.router)
app.include_router(loans.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Library Management API"
    }