from pydantic import BaseModel
from typing import Optional

class UserData(BaseModel):
    id: int
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserEdit(BaseModel):
    username: str
    email: str
    password: str
    biography: Optional[str]