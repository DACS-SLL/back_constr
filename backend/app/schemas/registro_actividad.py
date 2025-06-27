from pydantic import BaseModel
from datetime import datetime

class RegistroActividadBase(BaseModel):
    action: str

class RegistroActividadCreate(RegistroActividadBase):
    usuario_id: int

class RegistroActividad(RegistroActividadBase):
    id: int
    usuario_id: int
    fecha: datetime

    class Config:
        orm_mode = True
