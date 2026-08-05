"""
Configuración de la conexión a la base de datos.

Usa la variable de entorno DATABASE_URL. Configúrala con la cadena de
conexión de tu proyecto de Supabase (Project Settings → Database →
Connection string → URI). Si no está definida, cae en un archivo
SQLite local (cv_local.db) para poder desarrollar y probar sin
conexión a Supabase.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cv_local.db")

# Por si la cadena de conexión llega con el esquema "postgres://"
# (algunos proveedores lo usan), lo normalizamos a "postgresql://",
# que es lo que requiere SQLAlchemy 2.x.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite necesita este argumento extra para funcionar con FastAPI
# (que puede usar la conexión desde distintos hilos). Postgres no lo necesita.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: abre una sesión de base de datos por petición y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()