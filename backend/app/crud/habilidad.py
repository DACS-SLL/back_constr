from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.curriculum import Curriculum as CurriculumModel
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

def asignar_habilidad(db, curriculum_id: int, habilidad_id: int):
    curriculum = db.query(CurriculumModel).filter_by(id=curriculum_id).first()
    habilidad = db.query(Habilidad).filter_by(id=habilidad_id).first()
    if not curriculum or not habilidad:
        raise HTTPException(status_code=404, detail="No encontrado")
    curriculum.habilidades.append(habilidad)
    db.commit()
    return {"msg": "Habilidad asignada"}

def remover_habilidad(db, curriculum_id: int, habilidad_id: int):
    curriculum = db.query(CurriculumModel).filter_by(id=curriculum_id).first()
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum no encontrado")
    curriculum.habilidades = [h for h in curriculum.habilidades if h.id != habilidad_id]
    db.commit()
    return {"msg": "Habilidad removida"}
