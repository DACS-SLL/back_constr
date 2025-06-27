from sqlalchemy import Column, Integer, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class Notificacion(Base):
    __tablename__ = "notificacion"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    mensaje = Column(Text)
    leida = Column(Boolean, default=False)
    fecha_envio = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    usuario = relationship("Usuario", back_populates="notificaciones")
