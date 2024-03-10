from fastapi import APIRouter, Depends, HTTPException

from src.domain.contact import Contact
from src.services import db

from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""




"""
THIS ROUTES ARE PRIVATE
"""