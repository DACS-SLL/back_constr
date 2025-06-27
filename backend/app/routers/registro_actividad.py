from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.registro_actividad import RegistroActividad, RegistroActividadCreate
from app.crud import registro_actividad as crud
from app.core.database import get_db

router = APIRouter(prefix="/registros", tags=["Registros de Actividad"])

@router.get("/", response_model=List[RegistroActividad])
def listar_registros(db: Session = Depends(get_db)):
    return crud.get_registros(db)

@router.post("/", response_model=RegistroActividad)
def crear_registro(registro: RegistroActividadCreate, db: Session = Depends(get_db)):
    return crud.create_registro(db, registro)
