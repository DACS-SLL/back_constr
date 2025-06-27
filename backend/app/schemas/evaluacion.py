from pydantic import BaseModel
from typing import Optional

class EvaluacionBase(BaseModel):
    comentario: Optional[str]
    puntaje: Optional[int]

class EvaluacionCreate(EvaluacionBase):
    postulacion_id: int
    evaluador_id: int

class Evaluacion(EvaluacionBase):
    id: int
    postulacion_id: int
    evaluador_id: int

    class Config:
        orm_mode = True
