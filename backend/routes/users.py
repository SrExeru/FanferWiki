from fastapi import APIRouter

user_router = APIRouter(
    prefix='/user',
    tags=['Users']
)

