from fastapi import APIRouter, Depends, Response, HTTPException
from services.database import session_manager, DBSession
from models import User, Session
from schemas.auth import RegisterData, LoginData

from datetime import datetime, timezone, timedelta
from services.security import encode_jwt

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@auth_router.post('/register')
async def register (register_request: RegisterData = Depends(RegisterData.as_form), db: DBSession = Depends(session_manager.get_session)):
    new_user = User(**register_request.model_dump())
    
    new_user.hash_password()
    
    db.add(new_user)
    await db.commit()
    
    session = Session(
        user_id=new_user.id,
        refresh_token=new_user.email
    )

    db.add(session)
    await db.commit()    
    
    # To unificate session system in the future
    
    return new_user

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
    
    access_payload = {
        'sub': str(user.id),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=15) 
    }
    refresh_payload = {
        'sub': str(user.id),
        'exp': datetime.now(timezone.utc) + timedelta(days=30)
    }
    
    access_token = encode_jwt(access_payload)
    refresh_token = encode_jwt(refresh_payload)

    session = Session(
            user_id=user.id,
            refresh_token=refresh_token,
            expires_at=refresh_payload['exp']
        )
        
    db.add(session)
    await db.commit()
        
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True
    )
        
    return access_token