import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from src.domain.book import Book
from src.domain.user import User
from src.services import db
from src.services.security import get_current_user, require_role

# Define the root media directory and the subdirectory for media files
media_root_directory = 'media'  # The root directory where all media files are stored
book_media_directory = os.path.join(media_root_directory, 'books_media')  # Subdirectory for specific media files

router = APIRouter()

"""
Public Routes:
1. GET / - Retrieve all books from the database.
2. GET /{_id} - Retrieve a book by its ID.
"""


# Get all books from the database
@router.get('/', operation_id='get_all_book_public')
async def get_all_book_public() -> list[Book]:
    """
    Retrieve all books from the database.

    :return: A list of Book objects containing all the books in the database.
    """
    cursor = db.process.book.find()
    book_list = [Book(**document) for document in cursor]
    return book_list


# Get a book by its ID
@router.get('/{_id}', operation_id='get_book_by_id_public')
async def get_book_by_id_public(_id: str):
    """
    Retrieve a book by its ID from the database.

    :param _id: The ID of the book to be retrieved.
    :return: The Book object if found; otherwise, raises a 404 error.
    """
    cursor = db.process.book.find_one({'_id': _id})
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Book by ID: ({_id}) does not exist')
    return Book(**cursor)


"""
Private Routes:
1. GET /admin/ - Retrieve all books from the database (admin).
2. GET /admin/{_id} - Retrieve a book by its ID (admin).
3. POST / - Add a new book to the database (admin).
4. PUT /{_id} - Edit an existing book by its ID (admin).
5. DELETE /{_id} - Delete a book by its ID (admin).
"""


# Get all books from the database (admin only)
@router.get('/admin/', operation_id='get_all_book_private')
async def get_all_book_private(current_user: User = Depends(require_role('admin'))) -> list[Book]:
    """
    Retrieve all books from the database. Admin access only.

    :param current_user: The currently authenticated user.
    :return: A list of Book objects containing all the books in the database.
    """
    cursor = db.process.book.find()
    book_list = [Book(**document) for document in cursor]
    return book_list


# Get a book by its ID (admin only)
@router.get('/admin/{_id}', operation_id='get_book_by_id_private')
async def get_book_by_id_private(_id: str, current_user: User = Depends(require_role('admin'))):
    """
    Retrieve a book by its ID from the database. Admin access only.

    :param _id: The ID of the book to be retrieved.
    :param current_user: The currently authenticated user.
    :return: The Book object if found; otherwise, raises a 404 error.
    """
    cursor = db.process.book.find_one({'_id': _id})
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Book by ID: ({_id}) does not exist')
    return Book(**cursor)


# Add a new book to the database (admin only)
@router.post('/', operation_id='add_new_book_private')
async def add_new_book_private(book: Book, current_user: User = Depends(require_role('admin'))) -> Book | None:
    """
    Add a new book to the database. Admin access only.

    :param book: The Book object representing the new book to be added.
    :param current_user: The currently authenticated user.
    :return: The newly added Book object if successful; otherwise, returns None.
    """
    book_dict = book.dict(by_alias=True)
    insert_result = db.process.book.insert_one(book_dict)
    if insert_result.acknowledged:
        book_dict['_id'] = str(book_dict['_id'])
        return Book(**book_dict)
    return None


# Edit an existing book by its ID (admin only)
@router.put('/{_id}', operation_id='edit_book_by_id_private')
async def edit_book_by_id_private(_id: str, book: Book, current_user: User = Depends(require_role('admin'))):
    """
    Edit an existing book by its ID in the database. Admin access only.

    :param _id: The ID of the book to be edited.
    :param book: The updated Book object with the new data.
    :param current_user: The currently authenticated user.
    :return: The updated Book object if successful; otherwise, returns None.
    """
    book_dict = book.dict(by_alias=True)
    del book_dict['_id']
    cursor = db.process.book.update_one({'_id': _id}, {'$set': book_dict})
    if cursor.modified_count > 0:
        updated_document = db.process.book.find_one({'_id': _id})
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Book(**updated_document)
    return None


# Delete a book by its ID (admin only)
@router.delete("/{_id}", operation_id='delete_book_by_id_private')
async def delete_book_by_id_private(_id: str, current_user: User = Depends(require_role('admin'))):
    """
    Delete a book by its ID from the database. Admin access only.

    :param _id: The ID of the book to be deleted.
    :param current_user: The currently authenticated user.
    :return: A success message if the book is deleted; otherwise, raises a 404 error.
    """
    delete_results = db.process.book.delete_one({'_id': _id})
    if delete_results.deleted_count > 0:
        return {'message': 'Book deleted successfully'}
    raise HTTPException(status_code=404, detail=f'Book with ID: ({_id}) not found!')


"""
Media Routes:
1. POST / - Upload a media file.
2. GET /{filename} - Retrieve a media file by filename.
3. GET /images/ - List all media files.
4. DELETE /{filename} - Delete a media file by filename.
"""


# Upload a media file
@router.post("/media/")
async def upload_book_file(file: UploadFile = File(...), current_user: User = Depends(require_role('admin'))):
    """
    Upload a media file to the server.

    :param current_user:
    :param file: The file to be uploaded.
    :return: A success message indicating the file was uploaded.
    """
    try:
        upload_directory = book_media_directory
        os.makedirs(upload_directory, exist_ok=True)
        contents = await file.read()
        file_name = file.filename if file.filename else 'uploaded_file'
        file_path = os.path.join(upload_directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'There was an error uploading the file: {str(e)}')
    finally:
        await file.close()
    return {"message": f"Successfully uploaded {file_name} to {upload_directory}"}


# Retrieve a media file by filename
@router.get('/media/{filename}')
async def get_book_image(filename: str):
    """
    Retrieve a media file by filename from the 'about_me_media' directory.

    :param filename: The name of the file to be retrieved.
    :return: The file if found; otherwise, raises a 404 error.
    """
    file_path = os.path.join(book_media_directory, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        # Raise a 404 error if the file is not found
        raise HTTPException(status_code=404, detail='Image not found!')

    try:
        # Return the file as a response
        return FileResponse(file_path)
    except Exception as e:
        # Raise an HTTP 500 error if there was an issue serving the file
        raise HTTPException(status_code=500, detail=f'Error serving file: {str(e)}')


# List all media files
@router.get('/images/')
async def list_book_images(current_user: User = Depends(require_role('admin'))):
    """
    List all media files in the upload directory.

    :return: A list of filenames in the upload directory.
    """
    upload_directory = book_media_directory
    if not os.path.exists(upload_directory):
        raise HTTPException(status_code=404, detail='Upload directory not found!')
    image_names = [f for f in os.listdir(upload_directory) if os.path.isfile(os.path.join(upload_directory, f))]
    return {"images": image_names}


# Delete a media file by filename
@router.delete("/media/{filename}")
async def delete_book_image(filename: str, current_user: User = Depends(require_role('admin'))):
    """
    Delete a media file from the upload directory.

    :param current_user:
    :param filename: The name of the file to be deleted.
    :return: A success message if the file is deleted; otherwise, raises a 404 error.
    """
    upload_directory = book_media_directory
    file_path = os.path.join(upload_directory, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error deleting the file: {str(e)}")
    return {"message": f"Successfully deleted {filename} from {upload_directory}"}
