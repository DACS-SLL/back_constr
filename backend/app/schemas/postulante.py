from pydantic import BaseModel
from typing import Optional
from datetime import date

class PostulanteBase(BaseModel):
    nombre_completo: str
    fecha_nacimiento: Optional[date]
    telefono: Optional[str]

class PostulanteCreate(PostulanteBase):
    usuario_id: int

class Postulante(PostulanteBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True
