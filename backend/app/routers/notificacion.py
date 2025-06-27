from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.notificacion import Notificacion, NotificacionCreate
from app.crud import notificacion as crud
from app.core.database import get_db

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

@router.get("/", response_model=List[Notificacion])
def listar_notificaciones(db: Session = Depends(get_db)):
    return crud.get_notificaciones(db)

@router.post("/", response_model=Notificacion)
def crear_notificacion(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    return crud.create_notificacion(db, notificacion)
