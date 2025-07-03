from sqlalchemy.orm import Session
from app.models.oferta_laboral import OfertaLaboral
from app.schemas.oferta_laboral import OfertaLaboralCreate
from app.models.empresa import Empresa

def get_oferta(db: Session, oferta_id: int):
    return db.query(OfertaLaboral).filter(OfertaLaboral.id == oferta_id).first()

def get_ofertas(db: Session, categoria_id=None, empresa_id=None, nombre_empresa=None,
                estado=None, ubicacion=None, skip=0, limit=20):
    query = db.query(OfertaLaboral)

    if nombre_empresa:
        query = query.join(Empresa).filter(Empresa.nombre.ilike(f"%{nombre_empresa}%"))

    if categoria_id:
        query = query.filter(OfertaLaboral.categoria_id == categoria_id)

    if empresa_id:
        try:
            empresa_id = int(empresa_id)
            query = query.filter(OfertaLaboral.empresa_id == empresa_id)
        except ValueError:
            pass

    if estado:
        query = query.filter(OfertaLaboral.estado.ilike(f"%{estado}%"))

    if ubicacion:
        query = query.filter(OfertaLaboral.ubicacion.ilike(f"%{ubicacion}%"))


    return query.offset(skip).limit(limit).all()

def create_oferta(db: Session, oferta: OfertaLaboralCreate):
    db_oferta = OfertaLaboral(**oferta.dict())
    db.add(db_oferta)
    db.commit()
    db.refresh(db_oferta)
    return db_oferta

def delete_oferta(db: Session, oferta_id: int):
    oferta = get_oferta(db, oferta_id)
    if oferta:
        db.delete(oferta)
        db.commit()
    return oferta
