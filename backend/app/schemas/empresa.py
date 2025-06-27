from pydantic import BaseModel
from typing import Optional

class EmpresaBase(BaseModel):
    nombre: str
    rubro: Optional[str]
    direccion: Optional[str]
    descripcion: Optional[str]

class EmpresaCreate(EmpresaBase):
    usuario_id: int

class Empresa(EmpresaBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True
