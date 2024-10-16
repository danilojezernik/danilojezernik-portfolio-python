"""
Routes Overview:
1. GET / - Retrieve all comments from the database.
2. GET /{blog_id} - Retrieve all comments for a specific blog post from the database.
3. POST /{blog_id} - Add a new comment to a specific blog post in the database.
4. PUT /{blog_id}/{comment_id} - Edit an existing comment by its ID for a specific blog post.
5. DELETE /{blog_id}/{comment_id} - Delete a comment by its ID for a specific blog post.
"""
from fastapi import APIRouter, HTTPException, Query, Depends

from src.domain.comments import Comment
from src.domain.user import User
from src.services import db
from src.services.security import require_role, get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""


# This route gets all comments from the database
@router.get("/", operation_id="get_all_comments")
async def get_comments_for_post() -> list[Comment]:
    """
    This route handles the retrieval of all comments from the database

    :return: a list of Comment objects containing all the comments in the database
    """

    # Retrieve all comments from the database using the find method
    cursor = db.process.comments.find()

    # Create a list of Comment objects by unpacking data from each document retrieved
    return [Comment(**document) for document in cursor]


@router.get("/{blog_id}", operation_id="get_comments_of_post")
async def get_comments_for_blog_id(
        blog_id: str,
        limit: int = Query(10, gt=0),  # Default to 10 comments
        offset: int = Query(0, ge=0)  # Start from the 0th comment by default
):
    """
    This route handles the retrieval of comments for a specific post from the database.

    :param blog_id: The ID of the blog post to retrieve comments for
    :param limit: The number of comments to retrieve (default is 10)
    :param offset: The starting point for retrieval (default is 0)
    :return: A list of Comment objects containing the requested number of comments for the specified blog post
    """

    # Retrieve the total count of comments
    total_count = db.process.comments.count_documents({'blog_id': blog_id})

    # Retrieve comments for the specific blog post using the find method with a filter
    # Sort by datum_vnosa in descending order (newest comment first)
    cursor = db.process.comments.find({'blog_id': blog_id}).sort('datum_vnosa', -1).skip(offset).limit(limit)

    # Convert the cursor to a list of Comment objects
    comments = [Comment(**document) for document in cursor]

    # If no comments are found, raise a 404 error
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found")

    # Return the comments along with the total count
    return {
        'comments': comments,
        'total_count': total_count
    }


# This route adds a comment to a specific post
@router.post("/{blog_id}", operation_id="add_comments_to_specific_post")
async def add_comment_to_post(blog_id: str, comments: Comment, current_user: str = Depends(get_current_user)) -> Comment | None:
    """
    This route handles adding a new comment to a specific blog post

    :param current_user:
    :param blog_id: the ID of the blog post to add a comment to
    :param comments: the Comment object containing the details of the new comment
    :return: the added Comment object with its ID or None if the operation failed
    """

    # Convert Comment object to dictionary and add the blog_id
    comment_dict = comments.dict(by_alias=True)
    comment_dict['blog_id'] = blog_id

    # Insert the comment into the database
    insert_result = db.process.comments.insert_one(comment_dict)
    if insert_result.acknowledged:
        comment_dict['_id'] = str(insert_result.inserted_id)
        return Comment(**comment_dict)
    return None


"""
THIS ROUTES ARE PRIVATE
"""


# This route gets all comments from the database
@router.get("/admin/", operation_id="get_all_comments")
async def get_comments_for_post(current_user: User = Depends(require_role('admin'))) -> list[Comment]:
    """
    This route handles the retrieval of all comments from the database

    :return: a list of Comment objects containing all the comments in the database
    """

    # Retrieve all comments from the database using the find method
    cursor = db.process.comments.find()

    # Create a list of Comment objects by unpacking data from each document retrieved
    return [Comment(**document) for document in cursor]


# This route gets one comment by it's ID from the database
@router.get("/admin/{_id}", operation_id="get_comment_by_id")
async def get_comment_by_id(_id: str, current_user: User = Depends(require_role('admin'))) -> Comment:
    """
    This route handles the retrieval of a comment from the database

    :param current_user:
    :param _id: the ID of the comment post to retrieve comment
    :return: a Comment object containing comment for the specified comment
    """

    # Retrieve comments for the specific blog post using the find method with a filter
    cursor = db.process.comments.find_one({'_id': _id})

    # If no blog is found, return a 404 error with a relevant detail message
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'Comment by ID: ({_id}) does not exist')
    else:
        # Create a list of Comment objects by unpacking data from each document retrieved
        return Comment(**cursor)


# This route gets all comments of a specific post from the database
@router.get("/admin/{blog_id}", operation_id="get_comments_of_post")
async def get_comments_for_blog_id(blog_id: str, current_user: User = Depends(require_role('admin'))) -> list[Comment]:
    """
    This route handles the retrieval of all comments for a specific post from the database

    :param current_user:
    :param blog_id: the ID of the blog post to retrieve comments for
    :return: a list of Comment objects containing all comments for the specified blog post
    """

    # Retrieve comments for the specific blog post using the find method with a filter
    cursor = db.process.comments.find({'blog_id': blog_id})

    # Create a list of Comment objects by unpacking data from each document retrieved
    return [Comment(**document) for document in cursor]


# This route adds a comment to a specific post
@router.post("/admin/{blog_id}", operation_id="add_comments_to_specific_post")
async def add_comment_to_post(blog_id: str, comments: Comment, current_user: User = Depends(require_role('admin'))) -> Comment | None:
    """
    This route handles adding a new comment to a specific blog post

    :param current_user:
    :param blog_id: the ID of the blog post to add a comment to
    :param comments: the Comment object containing the details of the new comment
    :return: the added Comment object with its ID or None if the operation failed
    """

    # Convert Comment object to dictionary and add the blog_id
    comment_dict = comments.dict(by_alias=True)
    comment_dict['blog_id'] = blog_id

    # Insert the comment into the database
    insert_result = db.process.comments.insert_one(comment_dict)
    if insert_result.acknowledged:
        comment_dict['_id'] = str(insert_result.inserted_id)
        return Comment(**comment_dict)
    return None


# This route is to edit a blog by its ID
@router.put('/admin/{_id}', operation_id='edit_blog_by_id_private')
async def edit_blog_by_id_private(_id: str, comment: Comment, current_user: User = Depends(require_role('admin'))) -> Comment | None:
    """
    Handles the editing of a blog by its ID in the database.

    :param _id: The ID of the blog to be edited.
    :param comment: The updated Blog object with the new data.
    :param current_user: The current user, obtained from the authentication system.
    :return: If the blog is successfully edited, returns the updated Blog object; otherwise, returns None.
    """

    # Convert the Blog object to a dictionary
    comment_dict = comment.dict(by_alias=True)
    print(comment_dict)  # Add this before updating to ensure the data is being processed correctly

    # Delete the '_id' field from the blog dictionary to avoid updating the ID
    del comment_dict['_id']

    # Update the blog in the database using the update_one method
    cursor = db.process.comments.update_one({'_id': _id}, {'$set': comment_dict})

    # Check if the blog was successfully updated
    if cursor.modified_count > 0:
        # Retrieve the updated blog from the database
        updated_document = db.process.comments.find_one({'_id': _id})

        # Check if the updated blog exists
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Comment(**updated_document)

    # Return None if the blog was not updated
    return None


# This route edits a comment by its ID
@router.put("/admin/{blog_id}/{comment_id}", operation_id="edit_comment_by_id")
async def edit_comment(blog_id: str, comment_id: str, comments: Comment, current_user: User = Depends(require_role('admin'))) -> Comment | None:
    """
    This route handles editing an existing comment by its ID

    :param current_user:
    :param blog_id: the ID of the blog post the comment belongs to
    :param comment_id: the ID of the comment to be edited
    :param comments: the Comment object containing the updated details of the comment
    :return: the updated Comment object or None if the operation failed
    """

    # Convert Comment object to dictionary and remove the _id field
    comment_dict = comments.dict(by_alias=True)
    del comment_dict['_id']

    # Update the comment in the database
    cursor = db.process.comments.update_one({'_id': comment_id, 'blog_id': blog_id}, {'$set': comment_dict})
    if cursor.modified_count > 0:
        updated_document = db.process.comments.find_one({'_id': comment_id})
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Comment(**updated_document)
    return None


# This route deletes a comment by its ID
@router.delete("/admin/{blog_id}/{comment_id}", operation_id="delete_comment_by_id")
async def delete_comment(blog_id: str, comment_id: str, current_user: User = Depends(require_role('admin'))) -> dict:
    """
    This route handles deleting a comment by its ID

    :param current_user:
    :param blog_id: the ID of the blog post the comment belongs to
    :param comment_id: the ID of the comment to be deleted
    :return: a dictionary message indicating the result of the delete operation
    """

    # Delete the comment from the database
    delete_result = db.process.comments.delete_one({'_id': comment_id, 'blog_id': blog_id})
    if delete_result.deleted_count > 0:
        return {"message": "Comment deleted successfully"}
    else:
        return {"message": "Comment not found"}
