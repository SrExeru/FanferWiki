from services.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Text
from typing import Optional

class Community(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    __tablename__ = 'communities'