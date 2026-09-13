from fastapi import APIRouter, Depends, HTTPException
from services.database import session_manager, DBSession
from models import User
from schemas.auth import RegisterData, LoginData

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

    # To return access and refresh token in the future
    
    return new_user

@auth_router.post('/login')
async def login (login_request: LoginData = Depends(LoginData.as_form), db: DBSession = Depends(session_manager.get_session)):
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

    # To return access and refresh token in the future
        
    return user