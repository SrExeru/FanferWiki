from fastapi import APIRouter, Depends, HTTPException
from services.database import session_manager, AsyncSession
from sqlalchemy import select
from models import User
from schemas import user_schemas

user_router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@user_router.post('/', response_model=user_schemas.UserData)
async def register_user (register_request: user_schemas.UserCreate, db: AsyncSession = Depends(session_manager.get_session)):
    new_user = User(
        username=register_request.username,
        email=register_request.email,
        password=register_request.password # To hash in the future
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@user_router.get('/{user_id}', response_model=user_schemas.UserData)
async def get_user (user_id: int, db: AsyncSession = Depends(session_manager.get_session)):
    query = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user = query.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found.'
        )
    
    return user

@user_router.put('/{user_id}', response_model=user_schemas.UserData)
async def edit_user (user_id: int, edit_request: user_schemas.UserEdit, db: AsyncSession = Depends(session_manager.get_session)):
    query = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user = query.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found.'
        )
        
    user.username = edit_request.username
    user.email = edit_request.email
    user.password = edit_request.password
    user.biography = edit_request.biography
    
    await db.commit()
    await db.refresh(user)
    
    return user

@user_router.delete('/{user_id}')
async def delete_user (user_id: int, db: AsyncSession = Depends(session_manager.get_session)):
    query = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user = query.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found.'
        )
    
    await db.delete(user)
    await db.commit()
    
    return 'User deleted.'