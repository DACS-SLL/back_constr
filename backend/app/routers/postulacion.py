from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.postulacion import Postulacion, PostulacionCreate, PostulacionUpdate
from app.models.postulacion import Postulacion as PostulacionModel
from app.schemas.usuario import Usuario
from app.models.usuario import Usuario as UsuarioModel
from app.core.security import get_current_user
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

@router.get("/mias", response_model=List[Postulacion])
def listar_postulaciones_usuario(
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(get_current_user)
):
    print("Tipo de usuario:", type(usuario))
    return db.query(PostulacionModel).filter(PostulacionModel.postulante_id == usuario.id).all()

@router.patch("/{postulacion_id}", response_model=Postulacion)
def actualizar_postulacion(
    postulacion_id: int,
    datos: PostulacionUpdate,
    db: Session = Depends(get_db)
):
    postulacion = db.query(PostulacionModel).filter_by(id=postulacion_id).first()
    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    # Solo actualizamos los campos que vienen en el body
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(postulacion, campo, valor)

    db.commit()
    db.refresh(postulacion)
    return postulacion