from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

# Tabla intermedia
curriculum_habilidad = Table(
    "curriculum_habilidad",
    Base.metadata,
    Column("curriculum_id", Integer, ForeignKey("curriculum.id", ondelete="CASCADE"), primary_key=True),
    Column("habilidad_id", Integer, ForeignKey("habilidad.id", ondelete="CASCADE"), primary_key=True)
)

class Habilidad(Base):
    __tablename__ = "habilidad"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    curriculums = relationship("Curriculum", secondary=curriculum_habilidad, back_populates="habilidades")
