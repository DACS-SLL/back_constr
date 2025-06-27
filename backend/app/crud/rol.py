from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.schemas.rol import RolCreate

def get_all_roles(db: Session):
    return db.query(Rol).all()

def get_rol(db: Session, rol_id: int):
    return db.query(Rol).filter(Rol.id == rol_id).first()

def create_rol(db: Session, rol: RolCreate):
    nuevo_rol = Rol(**rol.dict())
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol

def delete_rol(db: Session, rol_id: int):
    db_rol = get_rol(db, rol_id)
    if db_rol:
        db.delete(db_rol)
        db.commit()
    return db_rol
