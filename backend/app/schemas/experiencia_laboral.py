from pydantic import BaseModel
from typing import Optional
from datetime import date

class ExperienciaLaboralBase(BaseModel):
    empresa: Optional[str]
    cargo: Optional[str]
    descripcion: Optional[str]
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]

class ExperienciaLaboralCreate(ExperienciaLaboralBase):
    curriculum_id: int

class ExperienciaLaboral(ExperienciaLaboralBase):
    id: int
    curriculum_id: int

    class Config:
        orm_mode = True
