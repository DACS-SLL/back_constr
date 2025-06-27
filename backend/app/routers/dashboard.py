# src/routers/dashboard.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, extract
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.oferta_laboral import OfertaLaboral
from app.models.postulacion import Postulacion
from app.models.postulante import Postulante
from app.models.entrevista import Entrevista
import calendar
from datetime import datetime, date


def normalizar_fecha(fecha):
    return datetime.combine(fecha, datetime.min.time()) if isinstance(fecha, date) and not isinstance(fecha, datetime) else fecha

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/actividad")
def actividad_reciente(rol: str = Query(...), db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    rol = rol.lower()
    eventos = []

    if rol == "postulante":
        postulaciones = (
            db.query(Postulacion)
            .filter(Postulacion.postulante_id == usuario.id)
            .order_by(Postulacion.fecha_postulacion.desc())
            .limit(5)
            .all()
        )

        oferta_ids = [p.oferta_id for p in postulaciones]

        entrevistas = (
            db.query(Entrevista)
            .options(
                joinedload(Entrevista.postulacion)
                .joinedload(Postulacion.postulante)
                .joinedload(Postulante.usuario)
            )
            .join(Entrevista.postulacion)
            .filter(Postulacion.oferta_id.in_(oferta_ids))
            .all()            
        )

        for p in postulaciones:
            eventos.append({
                "titulo": "Postulación enviada",
                "descripcion": f"Postulaste a: {p.oferta.titulo}",
                "fecha": p.fecha_postulacion,
                "color": "primary"
            })

        for e in entrevistas:
            eventos.append({
                "titulo": "Entrevista programada",
                "descripcion": f"Con {e.postulacion.oferta.empresa.nombre} el {e.fecha.date()}",
                "fecha": e.fecha,
                "color": "success"
            })

    elif rol == "empleador":
        ofertas = db.query(OfertaLaboral).filter_by(empresa_id=usuario.empresa.id).all()
        oferta_ids = [o.id for o in ofertas]

        postulaciones = (
            db.query(Postulacion)
            .filter(Postulacion.oferta_id.in_(oferta_ids))
            .order_by(Postulacion.fecha_postulacion.desc())
            .limit(5)
            .all()
        )

        entrevistas = (
            db.query(Entrevista)
            .options(
                joinedload(Entrevista.postulacion)
                .joinedload(Postulacion.postulante)
                .joinedload(Postulante.usuario)
            )
            .join(Entrevista.postulacion)
            .filter(Postulacion.oferta_id.in_(oferta_ids))
            .all()
        )

        for p in postulaciones:
            eventos.append({
                "titulo": "Nueva postulación recibida",
                "descripcion": f"{p.postulante.usuario.nombre} se postuló a: {p.oferta.titulo}",
                "fecha": p.fecha_postulacion,
                "color": "warning"
            })

        for e in entrevistas:
            eventos.append({
                "titulo": "Entrevista agendada",
                "descripcion": f"Entrevista con {e.postulacion.postulante.usuario.nombre}",
                "fecha": e.fecha,
                "color": "success"
            })

    elif rol == "admin":
        usuarios = (
            db.query(Usuario)
            .order_by(Usuario.fecha_registro.desc())
            .limit(5)
            .all()
        )

        for u in usuarios:
            eventos.append({
                "titulo": "Nuevo usuario registrado",
                "descripcion": f"{u.nombre} se unió como {u.rol.nombre}",
                "fecha": u.fecha_registro,
                "color": "info"
            })

    else:
        raise HTTPException(status_code=400, detail="Rol no válido")

    # Ordenar todos los eventos por fecha descendente
    eventos.sort(key=lambda x: normalizar_fecha(x["fecha"]), reverse=True)
    return eventos


@router.get("/resumen")
def obtener_resumen(rol: str = Query(...), db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    rol = rol.lower()

    if rol == "postulante":
        postulaciones = db.query(Postulacion).filter_by(postulante_id=usuario.id).count()

        entrevistas = (
            db.query(Entrevista)
            .join(Entrevista.postulacion)
            .filter(Postulacion.postulante_id == usuario.id)
            .count()
        )

        ofertas_disponibles = (
            db.query(OfertaLaboral).filter(OfertaLaboral.estado == "activa").count()
        )

        return {
            "postulaciones": postulaciones,
            "entrevistas": entrevistas,
            "ofertas_disponibles": ofertas_disponibles
        }


    elif rol == "empleador":
        ofertas = db.query(OfertaLaboral).filter_by(empresa_id=usuario.empresa.id).all()
        ofertas_ids = [o.id for o in ofertas]

        postulaciones = (
            db.query(Postulacion)
            .filter(Postulacion.oferta_id.in_(ofertas_ids))
            .count()
        )

        entrevistas = (
            db.query(Entrevista)
            .join(Entrevista.postulacion)
            .filter(Postulacion.oferta_id.in_(ofertas_ids))
            .count()
        )

        return {
            "ofertas_creadas": len(ofertas),
            "postulaciones_recibidas": postulaciones,
            "entrevistas_agendadas": entrevistas
        }


    elif rol == "admin":
        total_usuarios = db.query(Usuario).count()
        total_ofertas = db.query(OfertaLaboral).count()
        total_entrevistas = db.query(Entrevista).count()
        return {
            "total_usuarios": total_usuarios,
            "total_ofertas": total_ofertas,
            "total_entrevistas": total_entrevistas
        }

    else:
        raise HTTPException(status_code=400, detail="Rol no válido")

@router.get("/chart")
def obtener_datos_grafico(rol: str = Query(...), db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    rol = rol.lower()

    if rol == "postulante":
        resultados = (
            db.query(
                extract("month", Postulacion.fecha_postulacion).label("mes"),
                func.count().label("total")
            )
            .filter(Postulacion.postulante_id == usuario.id)
            .group_by("mes")
            .order_by("mes")
            .all()
        )

        meses = [calendar.month_name[int(r.mes)] for r in resultados]
        valores = [r.total for r in resultados]
        return {"meses": meses, "valores": valores}

    elif rol == "empleador":
        ofertas = db.query(OfertaLaboral).filter(OfertaLaboral.empresa_id == usuario.empresa.id).all()
        datos = []
        for oferta in ofertas:
            conteo = db.query(Postulacion).filter(Postulacion.oferta_id == oferta.id).count()
            datos.append((oferta.titulo, conteo))

        ofertas = [titulo for titulo, _ in datos]
        cantidades = [total for _, total in datos]
        return {"ofertas": ofertas, "cantidades": cantidades}

    elif rol == "admin":
        resultados = (
            db.query(
                extract("month", Usuario.fecha_registro).label("mes"),
                func.count().label("total")
            )
            .group_by("mes")
            .order_by("mes")
            .all()
        )

        meses = [calendar.month_name[int(r.mes)] for r in resultados]
        valores = [r.total for r in resultados]
        return {"meses": meses, "valores": valores}

    raise HTTPException(status_code=400, detail="Rol no válido")

@router.get("/tabla-reciente")
def tabla_reciente(rol: str = Query(...), db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    rol = rol.lower()

    if rol == "postulante":
        postulaciones = (
            db.query(Postulacion)
            .filter(Postulacion.postulante_id == usuario.id)
            .order_by(Postulacion.fecha_postulacion.desc())
            .limit(5)
            .all()
        )
        return {
            "columnas": ["Oferta", "Empresa", "Fecha"],
            "items": [
                {
                    "id": p.id,
                    "col1": p.oferta.titulo,
                    "col2": p.oferta.empresa.nombre,
                    "col3": p.fecha_postulacion.strftime("%d/%m/%Y"),
                }
                for p in postulaciones
            ]
        }

    elif rol == "empleador":
        ofertas = (
            db.query(OfertaLaboral)
            .filter(OfertaLaboral.empresa_id == usuario.empresa.id)
            .order_by(OfertaLaboral.fecha_publicacion.desc())
            .limit(5)
            .all()
        )
        return {
            "columnas": ["Título", "Descripción", "Fecha"],
            "items": [
                {
                    "id": o.id,
                    "col1": o.titulo,
                    "col2": o.descripcion,
                    "col3": o.fecha_publicacion.strftime("%d/%m/%Y"),
                }
                for o in ofertas
            ]
        }

    elif rol == "admin":
        usuarios = (
            db.query(Usuario)
            .order_by(Usuario.fecha_registro.desc())
            .limit(5)
            .all()
        )
        return {
            "columnas": ["Nombre", "Email", "Rol"],
            "items": [
                {
                    "id": u.id,
                    "col1": u.nombre,
                    "col2": u.email,
                    "col3": u.rol.nombre,
                }
                for u in usuarios
            ]
        }

    raise HTTPException(status_code=400, detail="Rol no válido")
