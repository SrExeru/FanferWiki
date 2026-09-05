from backend.services.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Text
from typing import Optional

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    
    biography: Mapped[Optional[str]] = mapped_column(Text)
    
    __tablename__ = 'users'