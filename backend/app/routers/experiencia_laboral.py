from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.experiencia_laboral import ExperienciaLaboral, ExperienciaLaboralCreate
from app.crud import experiencia_laboral as crud
from app.core.database import get_db

router = APIRouter(prefix="/experiencia", tags=["Experiencia Laboral"])

@router.get("/", response_model=List[ExperienciaLaboral])
def listar_experiencia(db: Session = Depends(get_db)):
    return crud.get_experiencias(db)

@router.post("/", response_model=ExperienciaLaboral)
def crear_experiencia(experiencia: ExperienciaLaboralCreate, db: Session = Depends(get_db)):
    return crud.create_experiencia(db, experiencia)
