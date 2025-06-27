from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.evaluacion import Evaluacion, EvaluacionCreate
from app.crud import evaluacion as crud
from app.core.database import get_db

router = APIRouter(prefix="/evaluaciones", tags=["Evaluaciones"])

@router.get("/", response_model=List[Evaluacion])
def listar_evaluaciones(
    entrevista_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return crud.get_evaluaciones(db, entrevista_id, skip, limit)

@router.post("/", response_model=Evaluacion)
def crear_evaluacion(evaluacion: EvaluacionCreate, db: Session = Depends(get_db)):
    return crud.create_evaluacion(db, evaluacion)
