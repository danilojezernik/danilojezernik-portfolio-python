import datetime

from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class LanguageData(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    tag: str
    count: int
    last_updated: datetime.datetime = Field(default_factory=datetime.datetime.now)

class LanguageDataResponse(BaseModel):
    tags: List[LanguageData]


class ErrorResponse(BaseModel):
    error_id: str
    error_message: str
    error_name: str