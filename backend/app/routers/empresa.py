from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.empresa import Empresa, EmpresaCreate
from app.crud import empresa as crud
from app.core.database import get_db

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.get("/", response_model=List[Empresa])
def listar_empresas(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_empresas(db, skip, limit)

@router.get("/{empresa_id}", response_model=Empresa)
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    return crud.get_empresa(db, empresa_id)

@router.post("/", response_model=Empresa)
def crear_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    return crud.create_empresa(db, empresa)
