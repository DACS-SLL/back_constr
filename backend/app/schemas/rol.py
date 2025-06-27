from pydantic import BaseModel

class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class Rol(RolBase):
    id: int
    nombre: str

    class Config:
        from_attributes = True
