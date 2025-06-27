from sqlalchemy.orm import Session
from app.models.educacion import Educacion
from app.schemas.educacion import EducacionCreate

def get_educacion(db: Session, educacion_id: int):
    return db.query(Educacion).filter(Educacion.id == educacion_id).first()

def get_educaciones(db: Session):
    return db.query(Educacion).all()

def create_educacion(db: Session, educacion: EducacionCreate):
    db_educacion = Educacion(**educacion.dict())
    db.add(db_educacion)
    db.commit()
    db.refresh(db_educacion)
    return db_educacion
