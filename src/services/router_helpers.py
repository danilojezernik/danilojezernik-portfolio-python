from typing import Type
from pydantic import BaseModel
from src.services import db


# All the data
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
    return [model(**document).dict(by_alias=True) for document in cursor]

# Data by ID
