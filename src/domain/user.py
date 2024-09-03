import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    username: str
    email: str
    full_name: str
    profession: str
    technology: str
    description: str
    hashed_password: str
    facebook: Optional[str]
    instagram: Optional[str]
    twitter: Optional[str]
    github: Optional[str]
    www: Optional[str]
    role: Optional[str] = 'visitor'
    confirmed: bool
    registered: Optional[bool] = False
    blog_notification: bool
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)
