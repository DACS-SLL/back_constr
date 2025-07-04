from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routers import (
    rol, usuario, postulante, habilidad, curriculum,
    empresa, categoria, oferta_laboral, postulacion,
    entrevista, evaluacion, educacion, experiencia_laboral,
    mensaje, notificacion, registro_actividad, auth, dashboard, admin_reports
)

# Crear tablas en la base de datos (solo en desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Empleo",
    description="API para gestionar ofertas, postulaciones, entrevistas y usuarios",
    version="1.0.0"
)

# Configuración CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # para Vue
    "https://front-constr.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://front-constr.vercel.app", "http://localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(rol.router)
app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(postulante.router)
app.include_router(habilidad.router)
app.include_router(curriculum.router)
app.include_router(empresa.router)
app.include_router(categoria.router)
app.include_router(oferta_laboral.router)
app.include_router(postulacion.router)
app.include_router(entrevista.router)
app.include_router(evaluacion.router)
app.include_router(educacion.router)
app.include_router(experiencia_laboral.router)
app.include_router(mensaje.router)
app.include_router(notificacion.router)
app.include_router(registro_actividad.router)
app.include_router(dashboard.router)
app.include_router(admin_reports.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Gestión de Empleo"}
