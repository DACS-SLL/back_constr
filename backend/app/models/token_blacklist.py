from sqlalchemy import Column, Integer, Text, String, TIMESTAMP
from app.core.database import Base
import datetime

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text, nullable=False)
    status = Column(String)
    fecha_revocado = Column(TIMESTAMP, default=datetime.datetime.utcnow)
