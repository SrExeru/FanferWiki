from fastapi import Form
from pydantic import BaseModel
from typing import Self

class RegisterData(BaseModel):
    username: str
    email: str
    password: str
        
    @classmethod
    def as_form (cls, username: str = Form(...), email: str = Form(...), password: str = Form(...)) -> Self:
        return cls(
            username=username,
            email=email,
            password=password
        )
        
class LoginData(BaseModel):
    email: str
    password : str
    
    @classmethod
    def as_form (cls, email: str = Form(...), password: str = Form(...)) -> Self:
        return cls(
            email=email,
            password=password
        )