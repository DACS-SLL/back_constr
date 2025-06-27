from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Entrevista(Base):
    __tablename__ = "entrevista"

    id = Column(Integer, primary_key=True, index=True)
    postulacion_id = Column(Integer, ForeignKey("postulacion.id"))
    fecha = Column(TIMESTAMP)
    resultado = Column(String)

    postulacion = relationship("Postulacion", back_populates="entrevistas")
