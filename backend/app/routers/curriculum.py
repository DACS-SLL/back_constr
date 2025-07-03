from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from app.schemas.curriculum import Curriculum, CurriculumCreate, CurriculumUpdate
from app.models.curriculum import Curriculum as CurriculumModel
from app.crud import curriculum as crud
from app.dependencies.auth import require_role
from app.core.database import get_db
from typing import List
from fastapi.responses import FileResponse
import os
from uuid import uuid4
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/curriculums", tags=["Curriculums"])
UPLOAD_DIR = "uploads/curriculums"

def get_curriculum_by_postulante(db: Session, postulante_id: int):
    return db.query(CurriculumModel)\
        .options(
            joinedload(CurriculumModel.educacion),
            joinedload(CurriculumModel.experiencia),
            joinedload(CurriculumModel.habilidades)
        )\
        .filter(CurriculumModel.postulante_id == postulante_id)\
        .first()


@router.get("/", response_model=List[Curriculum])
def listar_curriculums(
    postulante_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return crud.get_curriculums(db, postulante_id, skip, limit)


@router.post("/", response_model=Curriculum)
def crear_curriculum(curriculum: CurriculumCreate, db: Session = Depends(get_db),
                     _: dict = Depends(require_role("admin","postulante"))):
    return crud.create_curriculum(db, curriculum)

@router.post("/upload")
def subir_curriculum(
    postulante_id: int,
    archivo: UploadFile = File(...),
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    extension = archivo.filename.split('.')[-1]
    nuevo_nombre = f"{uuid4()}.{extension}"
    ruta_archivo = os.path.join(UPLOAD_DIR, nuevo_nombre)

    with open(ruta_archivo, "wb") as f:
        f.write(archivo.file.read())

    return {"ruta_archivo": ruta_archivo, "nombre_original": archivo.filename}


@router.get("/{curriculum_id}/download")
def descargar_curriculum(curriculum_id: int, db: Session = Depends(get_db)):
    curriculum = crud.get_curriculum(db, curriculum_id)
    if not curriculum:
        raise HTTPException(status_code=404, detail="No encontrado")
    return FileResponse(curriculum.ruta_archivo, filename=curriculum.nombre_original)

@router.get("/mio", response_model=Curriculum)
def obtener_mi_curriculum(
    db: Session = Depends(get_db),
    usuario = Depends(require_role("postulante"))
):
    return crud.get_curriculum_by_postulante(db, postulante_id=usuario["id"])

@router.put("/{curriculum_id}", response_model=Curriculum)
def actualizar_curriculum(
    curriculum_id: int,
    datos: CurriculumUpdate,
    db: Session = Depends(get_db),
    usuario = Depends(require_role("postulante"))
):
    return crud.update_curriculum(db, curriculum_id, datos, usuario.id)