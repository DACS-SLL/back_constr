from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.experiencia_laboral import ExperienciaLaboral, ExperienciaLaboralCreate
from app.crud import experiencia_laboral as crud
from app.core.database import get_db
from app.dependencies.auth import require_role
from app.models.experiencia_laboral import ExperienciaLaboral as ExperienciaLaboralModel

router = APIRouter(prefix="/experiencia", tags=["Experiencia Laboral"])

@router.get("/", response_model=List[ExperienciaLaboral])
def listar_experiencia(db: Session = Depends(get_db)):
    return crud.get_experiencias(db)

@router.post("/", response_model=ExperienciaLaboral)
def crear_experiencia(
    experiencia: ExperienciaLaboralCreate,
    db: Session = Depends(get_db),
    usuario: dict = Depends(require_role("postulante"))
):
    return crud.create_experiencia(db, experiencia, usuario.id)

@router.put("/{id}", response_model=ExperienciaLaboral)
def actualizar_experiencia(id: int, datos: ExperienciaLaboralCreate, db: Session = Depends(get_db)):
    return crud.update_experiencia(db, id, datos)

@router.delete("/{id}")
def eliminar_experiencia(id: int, db: Session = Depends(get_db)):
    return crud.delete_experiencia(db, id)
