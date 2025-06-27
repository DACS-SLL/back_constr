from sqlalchemy.orm import Session
from app.models.entrevista import Entrevista
from app.schemas.entrevista import EntrevistaCreate

def get_entrevista(db: Session, entrevista_id: int):
    return db.query(Entrevista).filter(Entrevista.id == entrevista_id).first()

def get_entrevistas(db: Session, postulacion_id=None, skip=0, limit=20):
    query = db.query(Entrevista)
    if postulacion_id:
        query = query.filter(Entrevista.postulacion_id == postulacion_id)
    return query.offset(skip).limit(limit).all()


def create_entrevista(db: Session, entrevista: EntrevistaCreate):
    db_entrevista = Entrevista(**entrevista.dict())
    db.add(db_entrevista)
    db.commit()
    db.refresh(db_entrevista)
    return db_entrevista
