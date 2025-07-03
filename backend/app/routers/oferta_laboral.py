from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.auth import require_role
from app.schemas.oferta_laboral import OfertaLaboral, OfertaLaboralCreate, OfertaLaboralOut, OfertaLaboralUpdate
from app.models.oferta_laboral import OfertaLaboral as OfertaLaboralModel
from app.crud import oferta_laboral as crud
from app.core.database import get_db

router = APIRouter(prefix="/ofertas", tags=["Ofertas Laborales"])

@router.get("/", response_model=List[OfertaLaboralOut])
def listar_ofertas(
    categoria_id: int | None = None,
    empresa_id: int | None = None,
    nombre_empresa: str | None = None,
    estado: str | None = None,
    ubicacion: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return crud.get_ofertas(db, categoria_id, empresa_id, nombre_empresa, estado, ubicacion, skip, limit)

@router.get("/{oferta_id}", response_model=OfertaLaboralOut)
def obtener_detalle_oferta(oferta_id: int, db: Session = Depends(get_db)):
    oferta = db.query(OfertaLaboralModel).filter(OfertaLaboralModel.id == oferta_id).first()
    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")
    return oferta

@router.post("/", response_model=OfertaLaboral)
def crear_oferta(oferta: OfertaLaboralCreate, db: Session = Depends(get_db),
                 _: dict = Depends(require_role("empleador", "admin"))):
    return crud.create_oferta(db, oferta)

@router.put("/{oferta_id}", response_model=OfertaLaboral)
def actualizar_oferta(oferta_id: int, oferta_actualizada: OfertaLaboralUpdate, db: Session = Depends(get_db),
                      _: dict = Depends(require_role("empleador", "admin"))):
    oferta = db.query(OfertaLaboralModel).filter(OfertaLaboralModel.id == oferta_id).first()
    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")
    
    for campo, valor in oferta_actualizada.dict(exclude_unset=True).items():
        setattr(oferta, campo, valor)

    db.commit()
    db.refresh(oferta)
    return oferta