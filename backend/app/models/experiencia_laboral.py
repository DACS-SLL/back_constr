from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ExperienciaLaboral(Base):
    __tablename__ = "experiencia_laboral"

    id = Column(Integer, primary_key=True, index=True)
    curriculum_id = Column(Integer, ForeignKey("curriculum.id"))
    empresa = Column(String)
    cargo = Column(String)
    descripcion = Column(Text)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)

    curriculum = relationship("Curriculum", back_populates="experiencia")
