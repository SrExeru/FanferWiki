from fastapi import APIRouter, Depends, HTTPException
from services.database import session_manager, DBSession
from services.security import auth_user
from models import User


profile_router = APIRouter(
    prefix='/profile',
    tags=['Profile']
)

@profile_router.get('/data')
def get_profile (user: User = Depends(auth_user)):
    # Profile settings
    
    pass