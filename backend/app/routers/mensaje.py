from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.mensaje import Mensaje, MensajeCreate
from app.crud import mensaje as crud
from app.core.database import get_db

router = APIRouter(prefix="/mensajes", tags=["Mensajes"])

@router.get("/", response_model=List[Mensaje])
def listar_mensajes(db: Session = Depends(get_db)):
    return crud.get_mensajes(db)

@router.post("/", response_model=Mensaje)
def crear_mensaje(mensaje: MensajeCreate, db: Session = Depends(get_db)):
    return crud.create_mensaje(db, mensaje)
