from sqlalchemy import Column, Integer, String

from database import Base


class DatosPersonalesDB(Base):
    __tablename__ = "datos_personales"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, default="")
    email = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    resumen = Column(String, nullable=True)


class ExperienciaLaboralDB(Base):
    __tablename__ = "experiencia_laboral"
    id = Column(Integer, primary_key=True, index=True)
    puesto = Column(String, nullable=False)
    empresa = Column(String, nullable=False)
    fecha_inicio = Column(String, nullable=True)
    fecha_fin = Column(String, nullable=True)
    descripcion = Column(String, nullable=True)


class FormacionAcademicaDB(Base):
    __tablename__ = "formacion_academica"
    id = Column(Integer, primary_key=True, index=True)
    institucion = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    fecha_inicio = Column(String, nullable=True)
    fecha_fin = Column(String, nullable=True)


class HabilidadDB(Base):
    __tablename__ = "habilidades"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    nivel = Column(String, nullable=True)