from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import require_role
from app.schemas.rol import Rol, RolCreate
from app.crud import rol as crud
from app.core.database import get_db
from typing import List

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[Rol])
def listar_roles(db: Session = Depends(get_db),
                    _: dict = Depends(require_role("admin"))):
    return crud.get_all_roles(db)

@router.post("/", response_model=Rol)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    return crud.create_rol(db, rol)
