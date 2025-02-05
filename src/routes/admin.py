"""
Route is used to get to the admin page where all the settings are
"""

from fastapi import APIRouter, Depends

from src.domain.user import User
from src.services.security import get_current_user

router = APIRouter()


# ADMIN PANEL
@router.post("/")
async def post(current_user: User = Depends(get_current_user)):
    return {'msg': 'Ste vpisani!'}
