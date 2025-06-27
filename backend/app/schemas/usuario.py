from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from .rol import Rol

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    email: EmailStr
    nombre: str
    contrasena: str
    rol_id: int

class Usuario(UsuarioBase):
    id: int
    activo: bool
    rol: Optional[Rol]

    class Config:
        from_attributes = True

class UsuarioRegistroCreate(BaseModel):
    email: EmailStr
    nombre: str
    contrasena: str = Field(..., min_length=8)
    confirmar_contrasena: str
    rol_id: int

    @validator("confirmar_contrasena")
    def validar_contrasenas_iguales(cls, v, values):
        if "contrasena" in values and v != values["contrasena"]:
            raise ValueError("Las contraseñas no coinciden")
        return v