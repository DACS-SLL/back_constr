from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificacionBase(BaseModel):
    mensaje: str
    leida: Optional[bool] = False

class NotificacionCreate(NotificacionBase):
    usuario_id: int

class Notificacion(NotificacionBase):
    id: int
    usuario_id: int
    fecha_envio: datetime

    class Config:
        orm_mode = True
