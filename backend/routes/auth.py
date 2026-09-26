from fastapi import APIRouter, Depends, Response, Cookie, HTTPException
from services.database import session_manager, DBSession
from models import User, Session
from schemas.auth import RegisterData, LoginData
from typing import Annotated

from datetime import datetime, timezone, timedelta
from services.security import encode_jwt, create_session

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@auth_router.post('/register')
async def register (response: Response, register_request: RegisterData = Depends(RegisterData.as_form), db: DBSession = Depends(session_manager.get_session)):
    new_user = User(**register_request.model_dump())
    
    new_user.hash_password()
    
    db.add(new_user)
    await db.commit()

    session_data = create_session(new_user.id)
            
    db.add(session_data.session)
    await db.commit()
        
    response.set_cookie(
        key='refresh_token',
        value=session_data.refresh_token,
        httponly=True
    )
        
    return session_data.access_token 

@auth_router.post('/login')
async def login (response: Response, login_request: LoginData = Depends(LoginData.as_form), db: DBSession = Depends(session_manager.get_session)):
    user = await db.select(User).where(User.email == login_request.email).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail='Icorrect email or password.'
        )
        
    if not user.verify_password(login_request.password):
        raise HTTPException(
            status_code=401,
            detail='Icorrect email or password.'
        )
        
        
    session_data = create_session(user.id)
        
    db.add(session_data.session)
    await db.commit()
        
    response.set_cookie(
        key='refresh_token',
        value=session_data.refresh_token,
        httponly=True
    )
        
    return session_data.access_token

@auth_router.get('/refresh')
async def refresh_session (response: Response, refresh_token: Annotated[str | None, Cookie()] = None, db: DBSession = Depends(session_manager.get_session)):
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail='Invalid session.'
        )
    # This is horrible now, i will fix this later
    session = await db.select(Session).where(Session.refresh_token == refresh_token).scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=401,
            detail='Invalid session.'
        )
        
    new_session = create_session(session.user_id)
    
    await db.delete(session)
    db.add(new_session.session)
    
    await db.commit()
    
    response.set_cookie(
        key='refresh_token',
        value=new_session.refresh_token,
        httponly=True
    )
            
    return new_session.access_token

@auth_router.post('/logout')
async def logout (response: Response, refresh_token: Annotated[str | None, Cookie()] = None, db: DBSession = Depends(session_manager.get_session)):
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail='Invalid session.'
        )
    # This is horrible now, i will fix this later
    session = await db.select(Session).where(Session.refresh_token == refresh_token).scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=401,
            detail='Invalid session.'
        )
    
    await db.delete(session)
    
    await db.commit()
    response.delete_cookie('refresh_token')

    return 'Completed logout.'