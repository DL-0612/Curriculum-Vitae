from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field


PATRON_FECHA = r"^\d{4}(-\d{1,2})?$"


class DatosPersonales(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre completo")
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(
        None, pattern=r"^[0-9+\-\s]{7,15}$",
        description="Solo dígitos, espacios, + o -, entre 7 y 15 caracteres"
    )
    ciudad: Optional[str] = None
    resumen: Optional[str] = Field(None, max_length=500)


class ExperienciaLaboral(BaseModel):
    puesto: str = Field(..., min_length=1)
    empresa: str = Field(..., min_length=1)
    fecha_inicio: Optional[str] = Field(None, pattern=PATRON_FECHA)
    fecha_fin: Optional[str] = Field(None, pattern=PATRON_FECHA)
    descripcion: Optional[str] = Field(None, max_length=500)


class FormacionAcademica(BaseModel):
    institucion: str = Field(..., min_length=1)
    titulo: str = Field(..., min_length=1)
    fecha_inicio: Optional[str] = Field(None, pattern=PATRON_FECHA)
    fecha_fin: Optional[str] = Field(None, pattern=PATRON_FECHA)


class Habilidad(BaseModel):
    nombre: str = Field(..., min_length=1)
    nivel: Optional[Literal["Básico", "Intermedio", "Avanzado"]] = None