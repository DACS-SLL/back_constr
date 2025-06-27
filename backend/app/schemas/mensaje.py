from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MensajeBase(BaseModel):
    contenido: str

class MensajeCreate(MensajeBase):
    emisor_id: int
    receptor_id: int

class Mensaje(MensajeBase):
    id: int
    emisor_id: int
    receptor_id: int
    fecha_envio: datetime

    class Config:
        orm_mode = True
