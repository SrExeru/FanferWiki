from services.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey, DateTime
import datetime

generate_date = lambda: datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)

class Session(Base):
    __tablename__='sessions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    refresh_token: Mapped[str] = mapped_column(String(800))
    expires_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=generate_date)