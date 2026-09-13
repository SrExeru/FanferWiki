from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.expression import ColumnElement, Select
from sqlalchemy import select
from typing import AsyncGenerator, Optional, Generic, Self, TypeVar, Sequence, Any, overload
from config import DATABASE_URL

class Base(DeclarativeBase):
    pass

# Database manager

M = TypeVar('M', bound=Base)
C = TypeVar('C', bound=ColumnElement[Any])
T = TypeVar('T')

# SELECT

class SelectConstructor(Generic[T]):
    def __init__(self, session: AsyncSession, entities: tuple[T, ...]) -> None:
        self.session: AsyncSession = session
        self.entities: Any = entities
        self.conditions: list[ColumnElement[bool]] = []
        
    def where(self, *conditions: ColumnElement[bool]) -> Self:
        self.conditions.extend(conditions)
        return self
    
    async def first(self) -> Optional[T]:
        stmt = self._build_query()
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def scalar_one_or_none(self) -> Optional[T]:
        stmt = self._build_query()
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def all(self) -> Sequence[T]:
        stmt = self._build_query()
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    def _build_query(self) -> Select:
        stmt = select(*self.entities).where(*self.conditions)
        
        return stmt
    
class DBSession():
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    def add(self, entity: Base) -> None:
        self.session.add(entity)
    
    async def commit(self) -> None:
        await self.session.commit()

    async def delete(self, *instances: object) -> None:
        for instance in instances:
            await self.session.delete(instance)
            
    @overload
    def select(self, *entities: type[M]) -> SelectConstructor[M]: ...
    
    @overload
    def select(self, *entities: C) -> SelectConstructor[C]: ...
    
    def select(self, *entities: Any) -> SelectConstructor[Any]:
            return SelectConstructor(self.session, entities)
            
            
# Database session service

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
        from models import all_models
        
        if self.engine is not None:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        
    async def close (self) -> None:
        if self.engine:
            await self.engine.dispose()
            
    async def get_session (self) -> AsyncGenerator[DBSession, None]:
        if not self.session_factory:
            raise RuntimeError("Database session factory is not initialized.")
        
        async with self.session_factory() as session:
            try:
                yield DBSession(session)
            except Exception:
                await session.rollback()
                raise
                
session_manager = SessionManager()


