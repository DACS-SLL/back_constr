from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.educacion import Educacion, EducacionCreate
from app.crud import educacion as crud
from app.core.database import get_db

router = APIRouter(prefix="/educacion", tags=["Educación"])

@router.get("/", response_model=List[Educacion])
def listar_educacion(db: Session = Depends(get_db)):
    return crud.get_educaciones(db)

@router.post("/", response_model=Educacion)
def crear_educacion(educacion: EducacionCreate, db: Session = Depends(get_db)):
    return crud.create_educacion(db, educacion)
