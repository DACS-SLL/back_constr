from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioRoleUpdate, UsuarioEstadoUpdate
from app.crud import usuario as crud
from app.core.database import get_db
from app.dependencies.auth import require_role
from app.core.security import get_current_user
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/me", response_model=Usuario)
def obtener_mi_perfil(current_user: Usuario = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=Usuario)
def actualizar_propio_usuario(usuario_update: UsuarioUpdate,
                              db: Session = Depends(get_db),
                              current_user: Usuario = Depends(get_current_user)):
    return crud.update_usuario(db, current_user.id, usuario_update)

@router.get("/", response_model=List[Usuario])
def listar_usuarios(skip: int = 0, limit: int = 20,
                    db: Session = Depends(get_db),
                    _: dict = Depends(require_role("admin"))):
    return crud.get_usuarios(db, skip, limit)

@router.get("/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int,
                    db: Session = Depends(get_db),
                    _: dict = Depends(require_role("admin"))):
    return crud.get_usuario(db, usuario_id)

@router.post("/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate,
                  db: Session = Depends(get_db)):
    return crud.create_usuario(db, usuario)


@router.put("/{usuario_id}/rol", response_model=Usuario)
def cambiar_rol_usuario(usuario_id: int, update: UsuarioRoleUpdate,
                        db: Session = Depends(get_db),
                        _: dict = Depends(require_role("admin"))):
    return crud.cambiar_rol(db, usuario_id, update.rol)

@router.put("/{usuario_id}/estado", response_model=Usuario)
def cambiar_estado_usuario(usuario_id: int, update: UsuarioEstadoUpdate,
                           db: Session = Depends(get_db),
                           _: dict = Depends(require_role("admin"))):
    return crud.cambiar_estado(db, usuario_id, update.activo)
