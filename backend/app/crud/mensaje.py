from sqlalchemy.orm import Session
from app.models.mensaje import Mensaje
from app.schemas.mensaje import MensajeCreate

def get_mensaje(db: Session, mensaje_id: int):
    return db.query(Mensaje).filter(Mensaje.id == mensaje_id).first()

def get_mensajes(db: Session):
    return db.query(Mensaje).all()

def create_mensaje(db: Session, mensaje: MensajeCreate):
    db_mensaje = Mensaje(**mensaje.dict())
    db.add(db_mensaje)
    db.commit()
    db.refresh(db_mensaje)
    return db_mensaje
