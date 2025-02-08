"""
This module provides helper functions for performing CRUD operations on a MongoDB database
using Pydantic models. Each function interacts with the database to retrieve, add, update,
or delete documents, while converting data to/from Pydantic models.

Functions:
- all_data: Retrieves all documents from a collection and converts them into Pydantic model instances.
- limited_data: Retrieves a limited number of documents from a collection and converts them into Pydantic model instances.
- data_by_id: Retrieves a single document by its _id from a collection and converts it into a Pydantic model instance.
- add_data: Inserts a new document into a collection and returns the newly created Pydantic model instance with its assigned _id.
- edit_data: Updates an existing document in a collection and returns the updated Pydantic model instance.
- delete_data: Deletes a document from a collection by its _id and returns a success message or raises an error if not found.
"""

from typing import Type
from pydantic import BaseModel
from src.services import db
from fastapi import HTTPException


# All the data: Retrieves all documents from a collection and converts them into Pydantic model instances.
def all_data(collection: str, model: Type[BaseModel]):
    """
    Retrieves all documents from the specified collection in the database and
    transforms each document into an instance of the provided Pydantic model.

    Parameters:
        collection (str): The name of the collection to query.
        model (Type[BaseModel]): The Pydantic model class to use for validation and transformation.

    Returns:
        List[model]: A list of Pydantic model instances representing each document.
    """
    cursor = db.process[collection].find()
    return [model(**document) for document in cursor]


# Limited data: Retrieves a limited number of documents from a collection and converts them into Pydantic model instances.
def limited_data(collection: str, model: Type[BaseModel], limit: int):
    """
    Retrieves a limited number of documents from the specified collection in the database and
    transforms each document into an instance of the provided Pydantic model.

    Parameters:
        collection (str): The name of the collection to query.
        model (Type[BaseModel]): The Pydantic model class to use for validation and transformation.
        limit (int): The maximum number of documents to retrieve.

    Returns:
        List[model]: A list of Pydantic model instances representing each document retrieved,
                     up to the specified limit.
    """
    cursor = db.process[collection].find().limit(limit)
    return [model(**document) for document in cursor]


# Data by ID: Retrieves a single document by its _id from a collection and converts it into a Pydantic model instance.
def data_by_id(collection: str, model: Type[BaseModel], _id: str):
    """
    Retrieves a single document from the specified collection by its ID and
    transforms it into an instance of the provided Pydantic model.

    Parameters:
        collection (str): The name of the collection to query.
        model (Type[BaseModel]): The Pydantic model class to use for validation and transformation.
        _id (str): The unique identifier of the document to retrieve.

    Returns:
        model: A Pydantic model instance representing the document.

    Raises:
        HTTPException: If a document with the provided ID is not found in the collection.
    """
    cursor = db.process[collection].find_one({'_id': _id})
    if cursor is None:
        raise HTTPException(status_code=404, detail=f'{collection} by ID: ({_id}) does not exist')
    else:
        return model(**cursor)


# Add new data: Inserts a new document into a collection and returns the created Pydantic model instance with its _id.
def add_data(collection: str, data: BaseModel, model: Type[BaseModel]):
    """
    Inserts a new document into the specified collection and returns a new model instance with the assigned _id.

    Parameters:
        collection (str): The name of the collection where the data will be inserted.
        data (BaseModel): The data to be inserted, represented as a Pydantic model instance.
        model (Type[BaseModel]): The Pydantic model class to use for returning the newly created instance.

    Returns:
        model | None: The newly created model instance (with the _id) if the insertion was successful; otherwise, None.
    """
    model_dict = data.dict(by_alias=True)
    insert_result = db.process[collection].insert_one(model_dict)
    if insert_result.acknowledged:
        model_dict['_id'] = str(insert_result.inserted_id)
        return model(**model_dict)
    else:
        return None


# Edit data: Updates an existing document in a collection with new data and returns the updated Pydantic model instance.
def edit_data(_id: str, collection: str, data: BaseModel, model: Type[BaseModel]):
    """
    Updates an existing document in the specified collection with new data and returns the updated document as a Pydantic model instance.

    Parameters:
        _id (str): The unique identifier of the document to be updated.
        collection (str): The name of the database collection where the document is stored.
        data (BaseModel): A Pydantic model instance containing the new data for the document.
        model (Type[BaseModel]): The Pydantic model class to use for validating and instantiating the updated document.

    Returns:
        An instance of the provided model containing the updated document if the update is successful.
        Returns None if the document was not modified or if the updated document cannot be retrieved.

    Process:
        1. Convert the provided data to a dictionary using field aliases.
        2. Remove the '_id' key from the dictionary to avoid attempting to update the immutable _id field.
        3. Use the $set operator to update the document in the collection.
        4. If the update modified the document, retrieve the updated document from the database.
        5. Convert the '_id' field to a string and return the updated document as an instance of the model.
        6. If no modifications were made, return None.
    """
    model_dict = data.dict(by_alias=True)
    del model_dict['_id']
    cursor = db.process[collection].update_one({'_id': _id}, {'$set': model_dict})
    if cursor.modified_count > 0:
        updated_document = db.process[collection].find_one({'_id': _id})
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return model(**updated_document)
    return None


# Delete data: Deletes a document from a collection by its _id and returns a success message, or raises an error if not found.
def delete_data(_id: str, collection: str):
    """
    Deletes a document from the specified collection in the database using its unique identifier.

    Parameters:
        _id (str): The unique identifier of the document to be deleted.
        collection (str): The name of the collection from which to delete the document.

    Returns:
        dict: A dictionary containing a success message if the document was deleted.

    Raises:
        HTTPException: If no document is found with the provided _id, a 404 error is raised.
    """
    delete_result = db.process[collection].delete_one({'_id': _id})
    if delete_result.deleted_count > 0:
        return {'message': f'{collection} deleted successfully!'}
    else:
        raise HTTPException(status_code=404, detail=f'{collection} by ID: ({_id}) not found!')
