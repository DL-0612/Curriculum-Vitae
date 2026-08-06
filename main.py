import os

from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from db_models import (
    DatosPersonalesDB,
    ExperienciaLaboralDB,
    FormacionAcademicaDB,
    HabilidadDB,
)
from models import DatosPersonales, ExperienciaLaboral, FormacionAcademica, Habilidad

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CV API",
    description="API RESTful para gestionar un Currículum Vítae (CRUD completo)",
    version="2.0.0"
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def manejador_errores_generales(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Error interno del servidor: {str(exc)}"}
    )


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))


app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


def orm_to_dict(obj) -> dict:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


def get_or_create_personal(db: Session) -> DatosPersonalesDB:
    personal = db.query(DatosPersonalesDB).filter(DatosPersonalesDB.id == 1).first()
    if not personal:
        personal = DatosPersonalesDB(id=1, nombre="Sin nombre")
        db.add(personal)
        db.commit()
        db.refresh(personal)
    return personal


@app.get("/cv", tags=["CV completo"])
def obtener_cv_completo(db: Session = Depends(get_db)):
    return {
        "datos_personales": orm_to_dict(get_or_create_personal(db)),
        "experiencia_laboral": [orm_to_dict(x) for x in db.query(ExperienciaLaboralDB).all()],
        "formacion_academica": [orm_to_dict(x) for x in db.query(FormacionAcademicaDB).all()],
        "habilidades": [orm_to_dict(x) for x in db.query(HabilidadDB).all()],
    }


@app.get("/cv/datos-personales", tags=["Datos personales"])
def obtener_datos_personales(db: Session = Depends(get_db)):
    return orm_to_dict(get_or_create_personal(db))


@app.put("/cv/datos-personales", tags=["Datos personales"])
def actualizar_datos_personales(datos: DatosPersonales, db: Session = Depends(get_db)):
    personal = get_or_create_personal(db)
    for campo, valor in datos.model_dump().items():
        setattr(personal, campo, valor)
    db.commit()
    db.refresh(personal)
    return orm_to_dict(personal)


@app.get("/cv/experiencia", tags=["Experiencia laboral"])
def listar_experiencia(db: Session = Depends(get_db)):
    return [orm_to_dict(x) for x in db.query(ExperienciaLaboralDB).all()]


@app.get("/cv/experiencia/{item_id}", tags=["Experiencia laboral"])
def obtener_experiencia(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ExperienciaLaboralDB).filter(ExperienciaLaboralDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia no encontrada")
    return orm_to_dict(item)


@app.post("/cv/experiencia", status_code=status.HTTP_201_CREATED, tags=["Experiencia laboral"])
def crear_experiencia(exp: ExperienciaLaboral, db: Session = Depends(get_db)):
    nuevo = ExperienciaLaboralDB(**exp.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return orm_to_dict(nuevo)


@app.put("/cv/experiencia/{item_id}", tags=["Experiencia laboral"])
def actualizar_experiencia(item_id: int, exp: ExperienciaLaboral, db: Session = Depends(get_db)):
    item = db.query(ExperienciaLaboralDB).filter(ExperienciaLaboralDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia no encontrada")
    for campo, valor in exp.model_dump().items():
        setattr(item, campo, valor)
    db.commit()
    db.refresh(item)
    return orm_to_dict(item)


@app.delete("/cv/experiencia/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Experiencia laboral"])
def eliminar_experiencia(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ExperienciaLaboralDB).filter(ExperienciaLaboralDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia no encontrada")
    db.delete(item)
    db.commit()
    return None


@app.get("/cv/formacion", tags=["Formación académica"])
def listar_formacion(db: Session = Depends(get_db)):
    return [orm_to_dict(x) for x in db.query(FormacionAcademicaDB).all()]


@app.get("/cv/formacion/{item_id}", tags=["Formación académica"])
def obtener_formacion(item_id: int, db: Session = Depends(get_db)):
    item = db.query(FormacionAcademicaDB).filter(FormacionAcademicaDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de formación no encontrado")
    return orm_to_dict(item)


@app.post("/cv/formacion", status_code=status.HTTP_201_CREATED, tags=["Formación académica"])
def crear_formacion(form: FormacionAcademica, db: Session = Depends(get_db)):
    nuevo = FormacionAcademicaDB(**form.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return orm_to_dict(nuevo)


@app.put("/cv/formacion/{item_id}", tags=["Formación académica"])
def actualizar_formacion(item_id: int, form: FormacionAcademica, db: Session = Depends(get_db)):
    item = db.query(FormacionAcademicaDB).filter(FormacionAcademicaDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de formación no encontrado")
    for campo, valor in form.model_dump().items():
        setattr(item, campo, valor)
    db.commit()
    db.refresh(item)
    return orm_to_dict(item)


@app.delete("/cv/formacion/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Formación académica"])
def eliminar_formacion(item_id: int, db: Session = Depends(get_db)):
    item = db.query(FormacionAcademicaDB).filter(FormacionAcademicaDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de formación no encontrado")
    db.delete(item)
    db.commit()
    return None


@app.get("/cv/habilidades", tags=["Habilidades"])
def listar_habilidades(db: Session = Depends(get_db)):
    return [orm_to_dict(x) for x in db.query(HabilidadDB).all()]


@app.get("/cv/habilidades/{item_id}", tags=["Habilidades"])
def obtener_habilidad(item_id: int, db: Session = Depends(get_db)):
    item = db.query(HabilidadDB).filter(HabilidadDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habilidad no encontrada")
    return orm_to_dict(item)


@app.post("/cv/habilidades", status_code=status.HTTP_201_CREATED, tags=["Habilidades"])
def crear_habilidad(hab: Habilidad, db: Session = Depends(get_db)):
    nuevo = HabilidadDB(**hab.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return orm_to_dict(nuevo)


@app.put("/cv/habilidades/{item_id}", tags=["Habilidades"])
def actualizar_habilidad(item_id: int, hab: Habilidad, db: Session = Depends(get_db)):
    item = db.query(HabilidadDB).filter(HabilidadDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habilidad no encontrada")
    for campo, valor in hab.model_dump().items():
        setattr(item, campo, valor)
    db.commit()
    db.refresh(item)
    return orm_to_dict(item)


@app.delete("/cv/habilidades/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Habilidades"])
def eliminar_habilidad(item_id: int, db: Session = Depends(get_db)):
    item = db.query(HabilidadDB).filter(HabilidadDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habilidad no encontrada")
    db.delete(item)
    db.commit()
    return None