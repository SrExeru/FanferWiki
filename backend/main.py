from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.database import session_manager, AsyncSession, Base
from contextlib import asynccontextmanager
import cloudinary
from config import cloudinaty_config, FRONTEND_URL

cloudinary.config(
    cloud_name=cloudinaty_config.CLOUDINARY_CLOUD_NAME,
    api_key=cloudinaty_config.CLOUDINARY_API_KEY,
    api_secret=cloudinaty_config.CLOUDINARY_API_SECRET,
    secure=True
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.init_db()
    
    await session_manager.load_models()
    
    yield
    
    await session_manager.close()

app = FastAPI(
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def hello_world():
    return 'Hello world!!'

from routes import all_routes

for route in all_routes:
    app.include_router(route)