from sqlalchemy.orm import Session
from app.models.educacion import Educacion
from app.schemas.educacion import EducacionCreate
from app.crud.curriculum import get_curriculum_id_by_postulante


def get_educacion(db: Session, educacion_id: int):
    return db.query(Educacion).filter(Educacion.id == educacion_id).first()

def get_educaciones(db: Session):
    return db.query(Educacion).all()

def create_educacion(db: Session, educacion: EducacionCreate, usuario_id: int):
    curriculum_id = get_curriculum_id_by_postulante(db, usuario_id)

    nueva = Educacion(
        curriculum_id=curriculum_id,
        institucion=educacion.institucion,
        titulo=educacion.titulo,
        fecha_inicio=educacion.fecha_inicio,
        fecha_fin=educacion.fecha_fin
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def update_educacion(db: Session, id: int, datos: EducacionCreate):
    educacion = db.query(Educacion).filter(Educacion.id == id).first()
    if not educacion:
        return None
    for campo, valor in datos.dict().items():
        setattr(educacion, campo, valor)
    db.commit()
    db.refresh(educacion)
    return educacion

def delete_educacion(db: Session, id: int):
    educacion = db.query(Educacion).filter(Educacion.id == id).first()
    if not educacion:
        return False
    db.delete(educacion)
    db.commit()
    return True
