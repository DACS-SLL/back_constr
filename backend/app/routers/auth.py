from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.core.security import crear_token_de_acceso, get_current_user
from app.schemas.usuario import UsuarioRegistroCreate, UsuarioCreate, Usuario
from app.models.rol import Rol
from app.models.usuario import Usuario as UsuarioModel
from app.crud.usuario import get_usuario_by_email, create_usuario
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Autenticación"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ROLES_PERMITIDOS = {"postulante", "empleador"}

@router.post("/register", response_model=Usuario)
def register(usuario: UsuarioRegistroCreate, db: Session = Depends(get_db)):
    db_user = get_usuario_by_email(db, usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")


    rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()

    if not rol:
        raise HTTPException(status_code=400, detail="Rol no válido")
    if rol.nombre not in ROLES_PERMITIDOS:
        raise HTTPException(status_code=403, detail="No se permite crear usuarios con este rol")
                            
    hashed_pwd = pwd_context.hash(usuario.contrasena)

    nuevo_usuario = UsuarioCreate(
        email=usuario.email,
        nombre=usuario.nombre,
        contrasena=pwd_context.hash(usuario.contrasena),
        rol_id=usuario.rol_id
    )
    return create_usuario(db, nuevo_usuario)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = get_usuario_by_email(db, email=form_data.username)
    if not usuario or not pwd_context.verify(form_data.password, usuario.contrasena_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    token = crear_token_de_acceso({"sub": str(usuario.id), "rol": usuario.rol.nombre})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=Usuario)
def get_current_user_info(current_user=Depends(get_current_user)):
    return current_user