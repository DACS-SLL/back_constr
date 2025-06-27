from sqlalchemy.orm import Session
from app.models.postulante import Postulante
from app.schemas.postulante import PostulanteCreate

def get_postulante(db: Session, postulante_id: int):
    return db.query(Postulante).filter(Postulante.id == postulante_id).first()

def get_postulantes(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Postulante).offset(skip).limit(limit).all()

def create_postulante(db: Session, postulante: PostulanteCreate):
    db_postulante = Postulante(**postulante.dict())
    db.add(db_postulante)
    db.commit()
    db.refresh(db_postulante)
    return db_postulante

def delete_postulante(db: Session, postulante_id: int):
    postulante = get_postulante(db, postulante_id)
    if postulante:
        db.delete(postulante)
        db.commit()
    return postulante
