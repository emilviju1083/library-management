# Library Management REST API

## Project Overview

The Library Management REST API is a backend application developed using Python, FastAPI, SQLAlchemy, and PostgreSQL.

This project helps manage library operations such as books, members, borrowing books, and returning books through REST API endpoints.

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Psycopg
- Uvicorn
- VS Code

## Project Structure

```text
library_management/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── books.py
│       ├── members.py
│       └── loans.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Database Design

The project uses a PostgreSQL database named `library_db`.

It contains three main tables:

### 1. Books
- book_id
- title
- author
- isbn
- category
- total_copies
- available_copies

### 2. Members
- member_id
- full_name
- email
- phone
- joined_date

### 3. Loans
- loan_id
- book_id
- member_id
- borrow_date
- due_date
- return_date
- status

## Features

### Book Management
- Add new books.
- View all books.
- View a book by ID.
- Update book details.
- Delete books.
- Prevent duplicate ISBN values.

### Member Management
- Register new members.
- View all members.
- View a member by ID.
- Update member information.
- Delete members.

### Loan Management
- Borrow books.
- Check book availability.
- Automatically decrease available copies when borrowing.
- Return borrowed books.
- Automatically increase available copies when returning.
- Track loan status and due dates.
- Prevent returning the same loan twice.

## Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the project folder

```bash
cd library_management
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Configure environment variables

Create a `.env` file in the project root directory.

Add your PostgreSQL connection details:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/library_db
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

### Step 7: Run the application

```bash
python -m uvicorn app.main:app --reload
```

The application will run at:

http://127.0.0.1:8000

## API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

## API Endpoints

### Books

| Method | Endpoint | Description |
|---|---|---|
| GET | /books/ | Get all books |
| GET | /books/{book_id} | Get book by ID |
| POST | /books/ | Add a new book |
| PUT | /books/{book_id} | Update a book |
| DELETE | /books/{book_id} | Delete a book |

### Members

| Method | Endpoint | Description |
|---|---|---|
| GET | /members/ | Get all members |
| GET | /members/{member_id} | Get member by ID |
| POST | /members/ | Register a member |
| PUT | /members/{member_id} | Update member |
| DELETE | /members/{member_id} | Delete member |

### Loans

| Method | Endpoint | Description |
|---|---|---|
| GET | /loans/ | Get all loans |
| GET | /loans/{loan_id} | Get loan by ID |
| POST | /loans/ | Borrow a book |
| PUT | /loans/{loan_id}/return | Return a book |

## Business Logic

1. A member can borrow a book if copies are available.
2. Available copies decrease when a book is borrowed.
3. Available copies increase when a book is returned.
4. A book cannot be borrowed when no copies are available.
5. A loan cannot be returned more than once.
6. Duplicate ISBN values and member email addresses are not allowed.

## Learning Outcomes

Through this project, I practised:

- Python backend development.
- REST API development using FastAPI.
- Database management using PostgreSQL.
- SQLAlchemy ORM.
- Pydantic data validation.
- CRUD operations.
- Database relationships and foreign keys.
- API testing using Swagger UI.
- Database transactions.

## Author

Developed as a Python backend development project.

