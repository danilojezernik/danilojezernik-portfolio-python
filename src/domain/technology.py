import datetime
from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field


class Technology(BaseModel):
    id: Optional[str] = Field(alias='_id', default_factory=lambda: str(ObjectId()))
    technology: str
    title: str
    subtitle: str
    vsebina: str
    image: Optional[List[str]] = None
    datum_vnosa: datetime.datetime = Field(default_factory=datetime.datetime.now)
