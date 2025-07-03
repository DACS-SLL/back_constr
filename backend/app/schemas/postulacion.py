from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from .postulante import Postulante as PostulanteSchema

class PostulacionBase(BaseModel):
    estado: Optional[str] = "pendiente"

class PostulacionCreate(PostulacionBase):
    postulante_id: int
    oferta_id: int    

class OfertaOut(BaseModel):
    id: int
    titulo: str
    descripcion: str
    ubicacion: str
    fecha_publicacion: date
class Postulacion(PostulacionBase):
    id: int
    postulante_id: int
    oferta: OfertaOut
    postulante: PostulanteSchema 
    fecha_postulacion: date    

    class Config:
        orm_mode = True

class PostulacionUpdate(BaseModel):
    estado: Optional[str] = None
    comentarios: Optional[str] = None
    fecha_postulacion: Optional[datetime] = None