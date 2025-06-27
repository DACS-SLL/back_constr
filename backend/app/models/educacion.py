from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Educacion(Base):
    __tablename__ = "educacion"

    id = Column(Integer, primary_key=True, index=True)
    curriculum_id = Column(Integer, ForeignKey("curriculum.id"))
    institucion = Column(String)
    titulo = Column(String)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)

    curriculum = relationship("Curriculum", back_populates="educacion")
