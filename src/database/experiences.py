import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Experiences(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    naslov: str
    stack: str
    company: str
    current: str
    company_start: str
    company_end: Optional[str]
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)
