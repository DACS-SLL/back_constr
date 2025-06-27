from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.usuario import Usuario, UsuarioCreate
from app.crud import usuario as crud
from app.core.database import get_db
from app.dependencies.auth import require_role
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=List[Usuario])
def listar_usuarios(skip: int = 0, limit: int = 20, db: Session = Depends(get_db),
                    _: dict = Depends(require_role("admin"))):
    return crud.get_usuarios(db, skip, limit)

@router.get("/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db),
                    _: dict = Depends(require_role("admin"))):
    return crud.get_usuario(db, usuario_id)

@router.post("/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db, usuario)
