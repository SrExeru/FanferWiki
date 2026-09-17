from dataclasses import dataclass
from os import getenv
from typing import Optional

def required_env (key: str) -> str:
    value = getenv(key)
    
    if not value:
        raise RuntimeError(f'Enviroment variables |Inexistent {key}')
    return value

DATABASE_URL = required_env('DATABASE_URL')
FRONTEND_URL = required_env('FRONTEND_URL')

JWT_SECRET = required_env('JWT_SECRET')
JWT_ALGORITHM = getenv('JWT_ALGORITHM', 'HS256')

@dataclass
class CloudinaryConfig:
    CLOUDINARY_CLOUD_NAME: Optional[str] = getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY: Optional[str] = getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET: Optional[str] = getenv('CLOUDINARY_API_SECRET')
    
cloudinaty_config = CloudinaryConfig()

