from sqlalchemy.orm import Session
from app.models.evaluacion import Evaluacion
from app.schemas.evaluacion import EvaluacionCreate

def get_evaluacion(db: Session, evaluacion_id: int):
    return db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()

def get_evaluaciones(db: Session, entrevista_id=None, skip=0, limit=20):
    query = db.query(Evaluacion)
    if entrevista_id:
        query = query.filter(Evaluacion.entrevista_id == entrevista_id)
    return query.offset(skip).limit(limit).all()

def create_evaluacion(db: Session, evaluacion: EvaluacionCreate):
    db_evaluacion = Evaluacion(**evaluacion.dict())
    db.add(db_evaluacion)
    db.commit()
    db.refresh(db_evaluacion)
    return db_evaluacion
