from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    contrasena_hash = Column(String, nullable=False)
    fecha_registro = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    activo = Column(Boolean, default=True)
    rol_id = Column(Integer, ForeignKey("rol.id"))

    rol = relationship("Rol", back_populates="usuarios")
    postulante = relationship("Postulante", back_populates="usuario", uselist=False)
    empresa = relationship("Empresa", back_populates="usuario", uselist=False)
    mensajes_enviados = relationship("Mensaje", back_populates="emisor", foreign_keys='Mensaje.emisor_id')
    mensajes_recibidos = relationship("Mensaje", back_populates="receptor", foreign_keys='Mensaje.receptor_id')
    notificaciones = relationship("Notificacion", back_populates="usuario")
    actividades = relationship("RegistroActividad", back_populates="usuario")
    evaluaciones = relationship("Evaluacion", back_populates="evaluador")
