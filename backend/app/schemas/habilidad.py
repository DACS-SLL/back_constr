from pydantic import BaseModel

class HabilidadBase(BaseModel):
    nombre: str

class HabilidadCreate(HabilidadBase):
    pass

class Habilidad(HabilidadBase):
    id: int

    class Config:
        orm_mode = True
