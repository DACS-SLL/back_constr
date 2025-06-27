from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class RegistroActividad(Base):
    __tablename__ = "registro_actividad"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    action = Column(String)
    fecha = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    usuario = relationship("Usuario", back_populates="actividades")
