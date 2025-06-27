from sqlalchemy.orm import Session
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate

def get_empresa(db: Session, empresa_id: int):
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

def get_empresas(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Empresa).offset(skip).limit(limit).all()

def create_empresa(db: Session, empresa: EmpresaCreate):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def delete_empresa(db: Session, empresa_id: int):
    empresa = get_empresa(db, empresa_id)
    if empresa:
        db.delete(empresa)
        db.commit()
    return empresa
