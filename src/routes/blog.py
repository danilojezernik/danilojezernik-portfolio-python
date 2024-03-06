"""
This module defines API routes for managing blogs

Routes:
1. GET all blogs
2. GET blog by ID
3. ADD a new blog
4. Edit (PUT) and existing blog by ID
5. DELETE a blog by ID
"""

from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def get_all_blogs():
    return {'page': 'Blogi'}
