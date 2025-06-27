from sqlalchemy.orm import Session
from app.models.habilidad import Habilidad
from app.schemas.habilidad import HabilidadCreate

def get_habilidad(db: Session, habilidad_id: int):
    return db.query(Habilidad).filter(Habilidad.id == habilidad_id).first()

def get_habilidades(db: Session):
    return db.query(Habilidad).all()

def create_habilidad(db: Session, habilidad: HabilidadCreate):
    db_habilidad = Habilidad(**habilidad.dict())
    db.add(db_habilidad)
    db.commit()
    db.refresh(db_habilidad)
    return db_habilidad
