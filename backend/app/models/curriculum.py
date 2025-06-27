from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from .habilidad import curriculum_habilidad
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class Curriculum(Base):
    __tablename__ = "curriculum"

    id = Column(Integer, primary_key=True, index=True)
    nombre_original = Column(String)
    postulante_id = Column(Integer, ForeignKey("postulante.id"))
    ruta_archivo = Column(String)
    fecha_subida = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    # Campos adicionales:
    resumen = Column(Text)
    competencias = Column(Text)
    idiomas = Column(String)
    linkedin_url = Column(String)
    github_url = Column(String)
    portafolio_url = Column(String)

    postulante = relationship("Postulante", back_populates="curriculum")
    educacion = relationship("Educacion", back_populates="curriculum")
    experiencia = relationship("ExperienciaLaboral", back_populates="curriculum")
    habilidades = relationship("Habilidad", secondary=curriculum_habilidad, back_populates="curriculums")