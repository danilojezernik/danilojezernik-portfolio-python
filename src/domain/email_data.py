import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class EmailData(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    full_name: str
    sender_email: str
    message: str
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)