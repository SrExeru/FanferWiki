from fastapi import APIRouter, Depends, HTTPException
from services.database import session_manager, AsyncSession
from sqlalchemy import select
from models import User
from schemas import user_schemas

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

auth_router.post('/login')
async def login (db: AsyncSession = Depends(session_manager.get_session)):
    pass