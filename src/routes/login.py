from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def get_login():
    return {'page': 'Login'}
