from sqlalchemy.orm import Session
from app.models.curriculum import Curriculum
from app.models.habilidad import Habilidad
from app.schemas.curriculum import CurriculumCreate

def get_curriculum(db: Session, curriculum_id: int):
    return db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()

def get_curriculums(db: Session, postulante_id=None, skip=0, limit=20):
    query = db.query(Curriculum)
    if postulante_id:
        query = query.filter(Curriculum.postulante_id == postulante_id)
    return query.offset(skip).limit(limit).all()

def create_curriculum(db: Session, curriculum: CurriculumCreate):
    habilidades_ids = curriculum.habilidades or []
    curriculum_data = curriculum.dict(exclude={"habilidades"})

    db_curriculum = Curriculum(**curriculum_data)

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
