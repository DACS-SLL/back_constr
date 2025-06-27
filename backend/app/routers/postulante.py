from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.postulante import Postulante, PostulanteCreate
from app.crud import postulante as crud
from app.core.database import get_db
from typing import List

router = APIRouter(prefix="/postulantes", tags=["Postulantes"])

@router.get("/", response_model=List[Postulante])
def listar_postulantes(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_postulantes(db, skip, limit)

@router.get("/{postulante_id}", response_model=Postulante)
def obtener_postulante(postulante_id: int, db: Session = Depends(get_db)):
    return crud.get_postulante(db, postulante_id)

@router.post("/", response_model=Postulante)
def crear_postulante(postulante: PostulanteCreate, db: Session = Depends(get_db)):
    return crud.create_postulante(db, postulante)
