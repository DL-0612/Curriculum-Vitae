"""
Punto de entrada para Vercel.

Vercel ejecuta funciones Python en un entorno tipo AWS Lambda, así que
no puede correr uvicorn directamente. Mangum adapta nuestra app ASGI
(FastAPI) a ese formato. Render/Railway NO necesitan este archivo
(ellos sí corren uvicorn normal); esto es exclusivo para Vercel.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from mangum import Mangum
from main import app

handler = Mangum(app)