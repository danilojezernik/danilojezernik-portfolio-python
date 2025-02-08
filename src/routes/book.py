"""
Book Routes:

Public Routes:
1. GET all books - Retrieve all books from the database.
2. GET book by ID - Retrieve a specific book by its ID.

Private Routes (Require authentication):
3. GET all books (private) - Retrieve all books for authenticated users.
4. GET book by ID (private) - Retrieve a specific book by its ID for authenticated users.
5. ADD a new book - Add a new book to the database.
6. EDIT a book by ID - Edit an existing book by its ID.
7. DELETE a book by ID - Delete a book by its ID.
"""

from fastapi import APIRouter, Depends
from src.domain.book import Book
from src.domain.user import User
from src.services.security import get_current_user
from src.utils.router_helpers import all_data, data_by_id, add_data, edit_data, delete_data

router = APIRouter()

# Public Routes

@router.get('/', operation_id='get_all_book_public')
async def get_all_book_public() -> list[Book]:
    """
    Retrieve all books from the database.
    """
    return all_data('book', Book)


@router.get('/{_id}', operation_id='get_book_by_id_public')
async def get_book_by_id_public(_id: str):
    """
    Retrieve a book by its ID from the database.
    """
    return data_by_id('book', Book, _id)


# Private Routes (Admin Only)

@router.get('/admin/', operation_id='get_all_book_private')
async def get_all_book_private(current_user: User = Depends(get_current_user)) -> list[Book]:
    """
    Retrieve all books from the database for authenticated (admin) users.
    """
    return all_data('book', Book)


@router.get('/admin/{_id}', operation_id='get_book_by_id_private')
async def get_book_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Retrieve a book by its ID for authenticated (admin) users.
    """
    return data_by_id('book', Book, _id)


@router.post('/', operation_id='add_new_book_private')
async def add_new_book_private(book: Book, current_user: User = Depends(get_current_user)) -> Book | None:
    """
    Add a new book to the database for authenticated (admin) users.
    """
    return add_data('book', book, Book)


@router.put('/{_id}', operation_id='edit_book_by_id_private')
async def edit_book_by_id_private(_id: str, book: Book, current_user: User = Depends(get_current_user)) -> Book | None:
    """
    Edit an existing book by its ID in the database for authenticated (admin) users.
    """
    return edit_data(_id, 'book', book, Book)


@router.delete("/{_id}", operation_id='delete_book_by_id_private')
async def delete_book_by_id_private(_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a book by its ID from the database for authenticated (admin) users.
    """
    return delete_data(_id, 'book')
