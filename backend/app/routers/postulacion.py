from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.postulacion import Postulacion, PostulacionCreate
from app.crud import postulacion as crud
from app.core.database import get_db

router = APIRouter(prefix="/postulaciones", tags=["Postulaciones"])

@router.get("/", response_model=List[Postulacion])
def listar_postulaciones(
    postulante_id: int | None = None,
    oferta_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return crud.get_postulaciones(db, postulante_id, oferta_id, skip, limit)

@router.post("/", response_model=Postulacion)
def crear_postulacion(postulacion: PostulacionCreate, db: Session = Depends(get_db)):
    return crud.create_postulacion(db, postulacion)
