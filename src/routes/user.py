from fastapi import APIRouter, Depends

from src.domain.user import User
from src.services import db
from src.services.security import get_current_user
router = APIRouter()


@router.get('/')
async def get_user(current_user: str = Depends(get_current_user)) -> list[User]:
    cursor = db.process.user.find()
    return [User(**document) for document in cursor]
