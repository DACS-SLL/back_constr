from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_usuario_by_id(db: Session, user_id: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        contrasena_hash=pwd_context.hash(usuario.contrasena),
        rol_id=usuario.rol_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    usuario = get_usuario(db, usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario

def update_usuario(db: Session, usuario_id: int, usuario_update: UsuarioUpdate) -> Usuario:
    usuario_db = get_usuario_by_id(db, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar campos condicionalmente
    if usuario_update.nombre is not None:
        usuario_db.nombre = usuario_update.nombre

    if usuario_update.email is not None:
        usuario_db.email = usuario_update.email

    if usuario_update.contrasena:
        contrasena_limpia = usuario_update.contrasena.strip()
        if contrasena_limpia:
            usuario_db.contrasena_hash = pwd_context.hash(contrasena_limpia)

    db.commit()
    db.refresh(usuario_db)
    return usuario_db

def cambiar_rol(db: Session, usuario_id: int, nuevo_rol: str):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    rol = db.query(Rol).filter(Rol.nombre == nuevo_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    usuario.rol_id = rol.id
    db.commit()
    db.refresh(usuario)
    return usuario


def cambiar_estado(db: Session, usuario_id: int, activo: bool):
    usuario = get_usuario(db, usuario_id)
    usuario.activo = activo
    db.commit()
    db.refresh(usuario)
    return usuario




