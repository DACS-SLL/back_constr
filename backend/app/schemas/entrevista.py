from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EntrevistaBase(BaseModel):
    fecha: Optional[datetime]
    resultado: Optional[str]

class EntrevistaCreate(EntrevistaBase):
    postulacion_id: int

class Entrevista(EntrevistaBase):
    id: int
    postulacion_id: int

    class Config:
        orm_mode = True
