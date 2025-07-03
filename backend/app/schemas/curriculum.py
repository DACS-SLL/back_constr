from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional, List
from .habilidad import Habilidad

class CurriculumBase(BaseModel):
    ruta_archivo: Optional[str] = Field(None, description="Ruta del archivo PDF en el servidor")
    nombre_original: Optional[str] = Field(None, description="Nombre original del archivo PDF")
    resumen: Optional[str] = Field('', description="Resumen profesional")
    competencias: Optional[str] = Field('', description="Competencias clave")
    idiomas: Optional[str] = Field('', description="Idiomas dominados")
    linkedin_url: Optional[HttpUrl] = Field(None, description="Enlace a LinkedIn")
    github_url: Optional[HttpUrl] = Field(None, description="Enlace a GitHub")
    portafolio_url: Optional[HttpUrl] = Field(None, description="Enlace a portafolio")

class CurriculumCreate(CurriculumBase):
    postulante_id: int = Field(..., description="ID del postulante")
    habilidades: Optional[List[int]] = Field(default_factory=list, description="IDs de habilidades seleccionadas")
class CurriculumUpdate(CurriculumBase):
    habilidades: Optional[List[int]]  # IDs de habilidades seleccionadas

class Curriculum(CurriculumBase):
    id: int
    postulante_id: int
    fecha_subida: datetime
    habilidades: List[Habilidad] = []

    class Config:
        orm_mode = True
