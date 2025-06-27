from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.entrevista import Entrevista, EntrevistaCreate
from app.crud import entrevista as crud
from app.core.database import get_db

router = APIRouter(prefix="/entrevistas", tags=["Entrevistas"])

@router.get("/", response_model=List[Entrevista])
def listar_entrevistas(
    postulacion_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return crud.get_entrevistas(db, postulacion_id, skip, limit)

@router.post("/", response_model=Entrevista)
def crear_entrevista(entrevista: EntrevistaCreate, db: Session = Depends(get_db)):
    return crud.create_entrevista(db, entrevista)
