from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.categoria import Categoria, CategoriaCreate
from app.crud import categoria as crud
from app.core.database import get_db

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=List[Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_categorias(db)

@router.post("/", response_model=Categoria)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db, categoria)
