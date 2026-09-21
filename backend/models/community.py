from services.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Text
from typing import Optional

class Community(Base):
    __tablename__ = 'communities'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), index=True, nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    icon_url: Mapped[Optional[str]] = mapped_column(String(300))
    icon_id: Mapped[Optional[str]] = mapped_column(String(300))