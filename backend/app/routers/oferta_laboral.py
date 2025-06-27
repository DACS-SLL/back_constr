from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.auth import require_role
from app.schemas.oferta_laboral import OfertaLaboral, OfertaLaboralCreate, OfertaLaboralOut
from app.crud import oferta_laboral as crud
from app.core.database import get_db

router = APIRouter(prefix="/ofertas", tags=["Ofertas Laborales"])

@router.get("/", response_model=List[OfertaLaboralOut])
def listar_ofertas(
    categoria_id: int | None = None,
    empresa_id: int | None = None,
    estado: str | None = None,
    ubicacion: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return crud.get_ofertas(db, categoria_id, empresa_id, estado, ubicacion, skip, limit)

@router.get("/{oferta_id}", response_model=OfertaLaboral)
def obtener_oferta(oferta_id: int, db: Session = Depends(get_db)):
    return crud.get_oferta(db, oferta_id)

@router.post("/", response_model=OfertaLaboral)
def crear_oferta(oferta: OfertaLaboralCreate, db: Session = Depends(get_db),
                 _: dict = Depends(require_role("empleador", "admin"))):
    return crud.create_oferta(db, oferta)
