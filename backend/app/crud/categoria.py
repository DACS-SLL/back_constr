from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate

def get_categoria(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()

def get_categorias(db: Session):
    return db.query(Categoria).all()

def create_categoria(db: Session, categoria: CategoriaCreate):
    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int):
    categoria = get_categoria(db, categoria_id)
    if categoria:
        db.delete(categoria)
        db.commit()
    return categoria
