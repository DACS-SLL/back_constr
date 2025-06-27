from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class Postulacion(Base):
    __tablename__ = "postulacion"

    id = Column(Integer, primary_key=True, index=True)
    postulante_id = Column(Integer, ForeignKey("postulante.id"))
    oferta_id = Column(Integer, ForeignKey("oferta_laboral.id"))
    fecha_postulacion = Column(Date, default=datetime.date.today)
    estado = Column(String, default="pendiente")

    postulante = relationship("Postulante", back_populates="postulaciones")
    oferta = relationship("OfertaLaboral", back_populates="postulaciones")
    entrevistas = relationship("Entrevista", back_populates="postulacion")
    evaluaciones = relationship("Evaluacion", back_populates="postulacion")
