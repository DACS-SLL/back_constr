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

class EmpresaOut(BaseModel):
    id: int
    nombre: str

class CategoriaOut(BaseModel):
    id: int
    nombre: str
class OfertaLaboralOut(BaseModel):
    id: int
    titulo: str
    descripcion: str
    fecha_publicacion: date
    ubicacion: str
    estado: str
    empresa: EmpresaOut
    categoria: CategoriaOut

    class Config:
        orm_mode = True

class OfertaLaboralUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None
    estado: Optional[str] = None
    categoria_id: Optional[int] = None
