from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class OfertaLaboral(Base):
    __tablename__ = "oferta_laboral"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"))
    titulo = Column(String, nullable=False)
    descripcion = Column(Text)
    ubicacion = Column(String)
    fecha_publicacion = Column(Date, default=datetime.date.today)
    categoria_id = Column(Integer, ForeignKey("categoria.id"))
    estado = Column(String, default="activa")

    empresa = relationship("Empresa", back_populates="ofertas")
    categoria = relationship("Categoria", back_populates="ofertas")
    postulaciones = relationship("Postulacion", back_populates="oferta")
