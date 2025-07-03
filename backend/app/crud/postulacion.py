from sqlalchemy.orm import Session
from app.models.postulacion import Postulacion
from sqlalchemy.orm import joinedload
from app.schemas.postulacion import PostulacionCreate

def get_postulacion(db: Session, postulacion_id: int):
    return db.query(Postulacion).filter(Postulacion.id == postulacion_id).first()

def get_postulaciones(db: Session, postulante_id=None, oferta_id=None, skip=0, limit=20):
    query = db.query(Postulacion).options(joinedload(Postulacion.postulante))  # 👈 JOIN

    if postulante_id:
        query = query.filter(Postulacion.postulante_id == postulante_id)
    if oferta_id:
        query = query.filter(Postulacion.oferta_id == oferta_id)

    return query.offset(skip).limit(limit).all()


def create_postulacion(db: Session, postulacion: PostulacionCreate):
    db_postulacion = Postulacion(**postulacion.dict())
    db.add(db_postulacion)
    db.commit()
    db.refresh(db_postulacion)
    return db_postulacion

def delete_postulacion(db: Session, postulacion_id: int):
    postulacion = get_postulacion(db, postulacion_id)
    if postulacion:
        db.delete(postulacion)
        db.commit()
    return postulacion
