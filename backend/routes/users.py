from fastapi import APIRouter, Depends, Cookie, HTTPException
from services.database import session_manager, DBSession
from models import User
from schemas.users import UserData, UserEdit

from services.security import decode_jwt

user_router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@user_router.get('/@me', response_model=UserData)
async def get_me (access_token: str, db: DBSession = Depends(session_manager.get_session)):
    payload = decode_jwt(access_token)
    
    user = await db.select(User).where(User.id == int(payload['sub'])).scalar_one_or_none()
        
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found.'
        )
    
    return user

@user_router.get('/{user_id}', response_model=UserData)
async def get_user (user_id: int, db: DBSession = Depends(session_manager.get_session)):
    user = await db.select(User).where(User.id == user_id).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found.'
        )
    
    return user

@user_router.put('/{user_id}', response_model=UserData)
async def edit_user (user_id: int, edit_request: UserEdit, db: DBSession = Depends(session_manager.get_session)):
    user = await db.select(User).where(User.id == user_id).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found.'
        )
        
    user.username = edit_request.username
    user.email = edit_request.email
    user.password = edit_request.password
    user.biography = edit_request.biography
    
    user.hash_password()
    
    await db.commit()
    
    return user

@user_router.delete('/{user_id}')
async def delete_user (user_id: int, db: DBSession = Depends(session_manager.get_session)):
    user = await db.select(User).where(User.id == user_id).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found.'
        )
    
    await db.delete(user)
    await db.commit()
    
    return 'User deleted.'