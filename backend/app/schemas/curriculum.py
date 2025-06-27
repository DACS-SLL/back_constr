from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List
from .habilidad import Habilidad

class CurriculumBase(BaseModel):
    ruta_archivo: Optional[str]
    resumen: Optional[str]
    competencias: Optional[str]
    idiomas: Optional[str]
    linkedin_url: Optional[HttpUrl]
    github_url: Optional[HttpUrl]
    portafolio_url: Optional[HttpUrl]

class CurriculumCreate(CurriculumBase):
    postulante_id: int
    habilidades: Optional[List[int]]  # IDs de habilidades seleccionadas

class Curriculum(CurriculumBase):
    id: int
    postulante_id: int
    fecha_subida: datetime
    habilidades: List[Habilidad] = []

    class Config:
        orm_mode = True
