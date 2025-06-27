from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class Mensaje(Base):
    __tablename__ = "mensaje"

    id = Column(Integer, primary_key=True, index=True)
    emisor_id = Column(Integer, ForeignKey("usuario.id"))
    receptor_id = Column(Integer, ForeignKey("usuario.id"))
    contenido = Column(Text)
    fecha_envio = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    emisor = relationship("Usuario", back_populates="mensajes_enviados", foreign_keys=[emisor_id])
    receptor = relationship("Usuario", back_populates="mensajes_recibidos", foreign_keys=[receptor_id])
