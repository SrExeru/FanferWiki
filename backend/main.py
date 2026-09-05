from fastapi import FastAPI
from backend.services.database import session_manager, AsyncSession, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.init_db()
    
    await session_manager.load_models()
    
    yield
    
    await session_manager.close()

app = FastAPI(
    lifespan=lifespan
)

@app.get('/')
async def hello_world():
    return 'Hello world!!'