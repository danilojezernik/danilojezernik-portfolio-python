from typing import Optional, List
import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

class User(BaseModel):
    name: str
    profile_image: str
    website_url: Optional[str]  # This might be null, so it's optional

class DevAritcle(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    type_of: str
    title: str
    description: str
    url: str
    cover_image: Optional[str]
    published_at: datetime.datetime
    tag_list: List[str]
    user: User
    last_updated: datetime.datetime = Field(default_factory=datetime.datetime.now)
