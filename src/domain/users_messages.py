import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Messages(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    user_id: str
    full_name_sender: str
    email_sender: str
    message: str
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)