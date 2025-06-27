from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Evaluacion(Base):
    __tablename__ = "evaluacion"

    id = Column(Integer, primary_key=True, index=True)
    postulacion_id = Column(Integer, ForeignKey("postulacion.id"))
    evaluador_id = Column(Integer, ForeignKey("usuario.id"))
    comentario = Column(Text)
    puntaje = Column(Integer)

    postulacion = relationship("Postulacion", back_populates="evaluaciones")
    evaluador = relationship("Usuario", back_populates="evaluaciones")
