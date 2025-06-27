from sqlalchemy.orm import Session
from app.models.registro_actividad import RegistroActividad
from app.schemas.registro_actividad import RegistroActividadCreate

def get_registro(db: Session, registro_id: int):
    return db.query(RegistroActividad).filter(RegistroActividad.id == registro_id).first()

def get_registros(db: Session):
    return db.query(RegistroActividad).all()

def create_registro(db: Session, registro: RegistroActividadCreate):
    db_registro = RegistroActividad(**registro.dict())
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro
