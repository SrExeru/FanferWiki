from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import DeclarativeBase
from backend.config import DATABASE_URL

class SessionManager:
    def __init__(self) -> None:
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None
        
    def init_db(self) -> None:
        if not DATABASE_URL:
            raise RuntimeError('Inexistent BATABASE_URL in enviroment variables.')
        
        self.engine = create_async_engine(
            DATABASE_URL,
            poolclass=AsyncAdaptedQueuePool
        )
        
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession
        )
        
    async def load_models (self):
        from backend.models import all_models
        
        if self.engine is not None:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        
    async def close (self) -> None:
        if self.engine:
            await self.engine.dispose()
            
    async def get_session (self) -> AsyncGenerator[AsyncSession, None]:
        if not self.session_factory:
            raise RuntimeError("Database session factory is not initialized.")
        
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
                
session_manager = SessionManager()
class Base(DeclarativeBase):
    pass