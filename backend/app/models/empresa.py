from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), unique=True)
    nombre = Column(String, nullable=False)
    rubro = Column(String)
    direccion = Column(String)
    descripcion = Column(Text)

    usuario = relationship("Usuario", back_populates="empresa")
    ofertas = relationship("OfertaLaboral", back_populates="empresa")
