from fastapi import APIRouter, Depends, HTTPException

from src.domain.experiences import Experiences
from src.services import db

from src.services.security import get_current_user

router = APIRouter()

"""
THIS ROUTES ARE PUBLIC
"""

# Get all the experiences from database
@router.get('/', operation_id='get_all_experiences')
async def get_all_experiences():
    cursor = db.process.experiences.find()
    experiences_list = [Experiences(**document) for document in cursor]
    return experiences_list

"""
THIS ROUTES ARE PRIVATE
"""