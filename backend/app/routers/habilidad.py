from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.habilidad import Habilidad, HabilidadCreate
from app.crud import habilidad as crud
from app.core.database import get_db
from typing import List

router = APIRouter(prefix="/habilidades", tags=["Habilidades"])

@router.get("/", response_model=List[Habilidad])
def listar_habilidades(db: Session = Depends(get_db)):
    return crud.get_habilidades(db)

@router.post("/", response_model=Habilidad)
def crear_habilidad(habilidad: HabilidadCreate, db: Session = Depends(get_db)):
    return crud.create_habilidad(db, habilidad)

@router.post("/asignar")
def asignar_habilidad_a_curriculum(
    curriculum_id: int,
    habilidad_id: int,
    db: Session = Depends(get_db)
):
    return crud.asignar_habilidad(db, curriculum_id, habilidad_id)

@router.delete("/remover")
def remover_habilidad_de_curriculum(
    curriculum_id: int,
    habilidad_id: int,
    db: Session = Depends(get_db)
):
    return crud.remover_habilidad(db, curriculum_id, habilidad_id)
