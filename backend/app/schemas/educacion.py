from pydantic import BaseModel
from typing import Optional
from datetime import date

class EducacionBase(BaseModel):
    institucion: Optional[str]
    titulo: Optional[str]
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]

class EducacionCreate(EducacionBase):
    curriculum_id: int

class Educacion(EducacionBase):
    id: int
    curriculum_id: int

    class Config:
        orm_mode = True
