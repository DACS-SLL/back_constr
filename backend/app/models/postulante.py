from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Postulante(Base):
    __tablename__ = "postulante"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), unique=True)
    nombre_completo = Column(String, nullable=False)
    fecha_nacimiento = Column(Date)
    telefono = Column(String)

    usuario = relationship("Usuario", back_populates="postulante")
    postulaciones = relationship("Postulacion", back_populates="postulante")
    curriculum = relationship("Curriculum", back_populates="postulante", uselist=False)
