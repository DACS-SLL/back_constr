from sqlalchemy.orm import Session
from app.models.experiencia_laboral import ExperienciaLaboral
from app.schemas.experiencia_laboral import ExperienciaLaboralCreate
from app.crud.curriculum import get_curriculum_id_by_postulante

def get_experiencia(db: Session, experiencia_id: int):
    return db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id == experiencia_id).first()

def get_experiencias(db: Session):
    return db.query(ExperienciaLaboral).all()

def create_experiencia(db: Session, experiencia: ExperienciaLaboralCreate, usuario_id: int):
    curriculum_id = get_curriculum_id_by_postulante(db, usuario_id)

    nueva = ExperienciaLaboral(
        curriculum_id=curriculum_id,
        empresa=experiencia.empresa,
        cargo=experiencia.cargo,
        descripcion=experiencia.descripcion,
        fecha_inicio=experiencia.fecha_inicio,
        fecha_fin=experiencia.fecha_fin,
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def update_experiencia(db: Session, id: int, datos: ExperienciaLaboralCreate):
    experiencia = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id == id).first()
    if not experiencia:
        return None
    for campo, valor in datos.dict().items():
        setattr(experiencia, campo, valor)
    db.commit()
    db.refresh(experiencia)
    return experiencia

def delete_experiencia(db: Session, id: int):
    experiencia = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id == id).first()
    if not experiencia:
        return False
    db.delete(experiencia)
    db.commit()
    return True
