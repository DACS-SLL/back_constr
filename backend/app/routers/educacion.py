from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.educacion import Educacion, EducacionCreate
from app.crud import educacion as crud
from app.dependencies.auth import require_role
from app.core.database import get_db

router = APIRouter(prefix="/educacion", tags=["Educación"])

@router.get("/", response_model=List[Educacion])
def listar_educacion(db: Session = Depends(get_db)):
    return crud.get_educaciones(db)

@router.post("/", response_model=Educacion)
def crear_educacion(
    educacion: EducacionCreate,
    db: Session = Depends(get_db),
    usuario: dict = Depends(require_role("postulante"))
):
    return crud.create_educacion(db, educacion, usuario.id)


@router.put("/{id}", response_model=Educacion)
def actualizar_educacion(id: int, datos: EducacionCreate, db: Session = Depends(get_db)):
    return crud.update_educacion(db, id, datos)

@router.delete("/{id}")
def eliminar_educacion(id: int, db: Session = Depends(get_db)):
    return crud.delete_educacion(db, id)
