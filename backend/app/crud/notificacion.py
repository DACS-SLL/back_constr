from sqlalchemy.orm import Session
from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionCreate

def get_notificacion(db: Session, notificacion_id: int):
    return db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()

def get_notificaciones(db: Session):
    return db.query(Notificacion).all()

def create_notificacion(db: Session, notificacion: NotificacionCreate):
    db_notificacion = Notificacion(**notificacion.dict())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion
