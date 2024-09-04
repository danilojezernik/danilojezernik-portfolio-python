from pydantic import BaseModel
from typing import Optional


class UserProfile(BaseModel):
    username: Optional[str]
    profession: Optional[str]
    full_name: Optional[str]
    description: Optional[str]
    email: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    twitter: Optional[str]
    github: Optional[str]
    www: Optional[str]
    blog_notification: Optional[bool]
    confirmed: Optional[bool]