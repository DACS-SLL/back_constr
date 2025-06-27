from pydantic import BaseModel
from typing import Optional
from datetime import date

class OfertaLaboralBase(BaseModel):
    titulo: str
    descripcion: Optional[str]
    ubicacion: Optional[str]
    estado: Optional[str] = "activa"

class OfertaLaboralCreate(OfertaLaboralBase):
    empresa_id: int
    categoria_id: int

class OfertaLaboral(OfertaLaboralBase):
    id: int
    empresa_id: int
    categoria_id: int
    fecha_publicacion: date

    class Config:
        orm_mode = True

class OfertaLaboralOut(BaseModel):
    id: int
    titulo: str
    descripcion: str
    fecha_publicacion: date
    ubicacion: str
    categoria_id: int
    estado: str

    class Config:
        orm_mode = True