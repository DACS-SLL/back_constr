from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.oferta_laboral import OfertaLaboral
from app.models.postulacion import Postulacion
from app.models.empresa import Empresa
from app.models.categoria import Categoria
from app.core.security import get_current_user
from app.dependencies.auth import require_role

router = APIRouter(prefix="/admin/reports", tags=["Admin Reports"])


@router.get("/ofertas-por-empresa")
def total_ofertas_por_empresa(db: Session = Depends(get_db),
                              _: dict = Depends(require_role("admin"))):
    resultados = (
        db.query(Empresa.nombre, func.count(OfertaLaboral.id))
        .join(OfertaLaboral, OfertaLaboral.empresa_id == Empresa.id)
        .group_by(Empresa.nombre)
        .all()
    )
    return [{"empresa": nombre, "total_ofertas": total} for nombre, total in resultados]


@router.get("/postulantes-por-oferta")
def postulantes_por_oferta(db: Session = Depends(get_db),
                           _: dict = Depends(require_role("admin"))):
    resultados = (
        db.query(OfertaLaboral.titulo, func.count(Postulacion.id))
        .join(Postulacion, Postulacion.oferta_id == OfertaLaboral.id)
        .group_by(OfertaLaboral.titulo)
        .all()
    )
    return [{"oferta": titulo, "total_postulantes": total} for titulo, total in resultados]


@router.get("/postulantes-por-categoria")
def postulantes_por_categoria(db: Session = Depends(get_db),
                              _: dict = Depends(require_role("admin"))):
    resultados = (
        db.query(Categoria.nombre, func.count(Postulacion.id))
        .join(OfertaLaboral, OfertaLaboral.categoria_id == Categoria.id)
        .join(Postulacion, Postulacion.oferta_id == OfertaLaboral.id)
        .group_by(Categoria.nombre)
        .all()
    )
    return [{"categoria": nombre, "total_postulantes": total} for nombre, total in resultados]


@router.get("/ofertas-por-estado")
def ofertas_por_estado(db: Session = Depends(get_db),
                       _: dict = Depends(require_role("admin"))):
    resultados = (
        db.query(OfertaLaboral.estado, func.count())
        .group_by(OfertaLaboral.estado)
        .all()
    )
    return [{"estado": estado, "total": total} for estado, total in resultados]


@router.get("/promedio-postulaciones")
def promedio_postulaciones_por_oferta(db: Session = Depends(get_db),
                                      _: dict = Depends(require_role("admin"))):
    total_postulaciones = db.query(func.count(Postulacion.id)).scalar()
    total_ofertas = db.query(func.count(OfertaLaboral.id)).scalar()

    promedio = round(total_postulaciones / total_ofertas, 2) if total_ofertas > 0 else 0.0
    return {"promedio_postulaciones_por_oferta": promedio}
