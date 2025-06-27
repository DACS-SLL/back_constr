from sqlalchemy.orm import Session
from app.models.experiencia_laboral import ExperienciaLaboral
from app.schemas.experiencia_laboral import ExperienciaLaboralCreate

def get_experiencia(db: Session, experiencia_id: int):
    return db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id == experiencia_id).first()

def get_experiencias(db: Session):
    return db.query(ExperienciaLaboral).all()

def create_experiencia(db: Session, experiencia: ExperienciaLaboralCreate):
    db_experiencia = ExperienciaLaboral(**experiencia.dict())
    db.add(db_experiencia)
    db.commit()
    db.refresh(db_experiencia)
    return db_experiencia
