from pydantic import BaseModel
from datetime import date
from typing import Optional

class PostulacionBase(BaseModel):
    estado: Optional[str] = "pendiente"

class PostulacionCreate(PostulacionBase):
    postulante_id: int
    oferta_id: int

class Postulacion(PostulacionBase):
    id: int
    postulante_id: int
    oferta_id: int
    fecha_postulacion: date

    class Config:
        orm_mode = True
