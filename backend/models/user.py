from services.database import Base
from sqlalchemy.orm import mapped_column, Mapped, validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import String, Text
from pwdlib import PasswordHash
from typing import Optional

password_hash = PasswordHash.recommended()

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    
    biography: Mapped[Optional[str]] = mapped_column(Text)
    
    def hash_password (self) -> None:
        self.password = password_hash.hash(self.password)
    
    def verify_password (self, plain_password: str) -> bool:
        return password_hash.verify(plain_password, self.password)