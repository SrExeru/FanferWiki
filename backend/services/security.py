from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.database import DBSession, session_manager
from models import User, Session
from config import JWT_SECRET, JWT_ALGORITHM
from jwt import encode, decode
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

# JWT

def encode_jwt(payload: dict[str, str]) -> str:
    return encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

def decode_jwt(encoded_jwt: str) -> dict[str, str]:
    return decode(
        encoded_jwt,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM]
    )
    
# Session system

@dataclass
class SessionData:
    refresh_token: str
    access_token: str
    session: Session
    
def create_session (user_id: int) -> SessionData:
    refresh_payload = {
        'sub': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=15) 
    }
    access_payload = {
        'sub': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(days=30) 
    }
    
    refresh_token = encode_jwt(refresh_payload)
    access_token = encode_jwt(access_payload)
    
    session = Session(
        user_id=user_id,
        refresh_token=refresh_token,
        expires_at=refresh_payload['exp']
    )
    
    return SessionData(
        refresh_token=refresh_token,
        access_token=access_token,
        session=session
    )

# Identify user

request_token = HTTPBearer()

async def auth_user (credentials: HTTPAuthorizationCredentials = Depends(request_token), db: DBSession = Depends(session_manager.get_session)):
    access_token = credentials.credentials
    
    if access_token.startswith("Bearer "):
        access_token = access_token.split(" ")[1]

    payload = decode_jwt(access_token)
    
    user_id = payload.get('sub')
    
    if not user_id or not user_id.isnumeric():
        raise HTTPException(
            status_code=400,
            detail='Invalid id.'
        )
    
    user = await db.select(User).where(User.id==int(user_id)).scalar_one_or_none()
    
    return user