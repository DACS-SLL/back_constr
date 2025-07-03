from sqlalchemy.orm import Session
from app.models.curriculum import Curriculum as CurriculumModel
from app.models.habilidad import Habilidad
from app.schemas.curriculum import CurriculumCreate, CurriculumUpdate
from fastapi import HTTPException


def get_curriculum(db: Session, curriculum_id: int):
    return db.query(CurriculumModel).filter(CurriculumModel.id == curriculum_id).first()

def get_curriculums(db: Session, postulante_id=None, skip=0, limit=20):
    query = db.query(CurriculumModel)
    if postulante_id:
        query = query.filter(CurriculumModel.postulante_id == postulante_id)
    return query.offset(skip).limit(limit).all()

def create_curriculum(db: Session, curriculum: CurriculumCreate):
    habilidades_ids = curriculum.habilidades or []
    curriculum_data = curriculum.dict(exclude={"habilidades"})

    db_curriculum = CurriculumModel(**curriculum_data)

    # Asociar habilidades
    db_curriculum.habilidades = db.query(Habilidad).filter(Habilidad.id.in_(habilidades_ids)).all()

    db.add(db_curriculum)
    db.commit()
    db.refresh(db_curriculum)
    return db_curriculum

def delete_curriculum(db: Session, curriculum_id: int):
    curriculum = get_curriculum(db, curriculum_id)
    if curriculum:
        db.delete(curriculum)
        db.commit()
    return curriculum

def update_curriculum(db: Session, curriculum_id: int, datos: CurriculumUpdate, usuario_id: int):
    curriculum = db.query(CurriculumModel).filter(
        CurriculumModel.id == curriculum_id,
        CurriculumModel.postulante_id == usuario_id
    ).first()

    if not curriculum:
        raise HTTPException(status_code=404, detail="Currículum no encontrado")

    habilidades_ids = datos.habilidades or []

    for campo, valor in datos.dict(exclude_unset=True, exclude={"habilidades"}).items():
        setattr(curriculum, campo, valor)

    # Asignar habilidades como objetos, no como IDs
    curriculum.habilidades = db.query(Habilidad).filter(Habilidad.id.in_(habilidades_ids)).all()

    db.commit()
    db.refresh(curriculum)
    return curriculum


def get_curriculum_by_postulante(db: Session, postulante_id: int):
    return db.query(CurriculumModel).filter(CurriculumModel.postulante_id == postulante_id).first()

def get_curriculum_id_by_postulante(db: Session, postulante_id: int) -> int:
    curriculum = db.query(CurriculumModel).filter_by(postulante_id=postulante_id).first()
    if not curriculum:
        raise HTTPException(status_code=404, detail="Currículum no encontrado")
    return curriculum.id