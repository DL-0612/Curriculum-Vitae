# CV API

API RESTful para gestionar un Currículum Vítae (CV): datos personales,
experiencia laboral, formación académica y habilidades. CRUD completo
sobre las 4 secciones, con persistencia en PostgreSQL.

Incluye además una página web (`static/index.html`) que consume la API
y muestra el CV de forma visual.

## Stack

- **Framework:** FastAPI
- **Base de datos:** PostgreSQL (producción) / SQLite (desarrollo local, automático)
- **ORM:** SQLAlchemy
- **Validación:** Pydantic

## Estructura del proyecto

```
cv_api/
├── main.py            # Endpoints de la API
├── database.py         # Configuración de conexión a la base de datos
├── db_models.py         # Modelos ORM (tablas)
├── models.py            # Modelos Pydantic (validación de entrada)
├── requirements.txt
├── Procfile              # Comando de arranque para Render/Railway
├── .env.example           # Variables de entorno de ejemplo
└── static/
    └── index.html          # Frontend que consume la API
```

## Configuración local

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. (Opcional) Copia `.env.example` a `.env` y ajusta `DATABASE_URL` si
   quieres usar Postgres en local. **Si no defines `DATABASE_URL`, la
   API usa automáticamente un archivo SQLite local (`cv_local.db`)**,
   así que este paso no es obligatorio para desarrollar.

3. Corre el servidor:
   ```bash
   python -m uvicorn main:app --reload
   ```

4. Abre `http://127.0.0.1:8000/` (interfaz visual) o
   `http://127.0.0.1:8000/docs` (documentación interactiva Swagger).

## Variables de entorno

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DATABASE_URL` | En producción sí | Cadena de conexión a la base de datos PostgreSQL de Supabase. Formato: `postgresql://postgres:[password]@db.xxxxxxxxxxxx.supabase.co:5432/postgres`. Si no se define, se usa SQLite local. |
| `ALLOWED_ORIGINS` | No | Orígenes permitidos para CORS, separados por coma. Por defecto `*` (cualquier origen). |

**Nunca subas tu archivo `.env` real ni credenciales a GitHub** — está
incluido en `.gitignore`.

## Base de datos: Supabase

1. Crea una cuenta en [supabase.com](https://supabase.com) y un **New project**
   (elige una contraseña para la base de datos y guárdala, la necesitarás
   en el paso 3).
2. Espera a que el proyecto termine de aprovisionarse (1-2 minutos).
3. Ve a **Project Settings → Database → Connection string**, pestaña
   **URI**. Copia esa cadena y reemplaza `[YOUR-PASSWORD]` por la
   contraseña que elegiste — esta es tu `DATABASE_URL`.
4. (Opcional) Si tu hosting reporta error de "too many connections",
   usa en su lugar la URI del **Connection pooler** (mismo panel,
   puerto `6543`) — está pensada para muchas conexiones simultáneas.

Las tablas se crean solas la primera vez que arranca la API
(`Base.metadata.create_all` en `main.py`) — no necesitas correr ningún
script SQL manualmente. Si quieres verlas, en Supabase ve a
**Table Editor**.

## Despliegue en Render

1. Sube este proyecto a un repositorio de GitHub.
2. En Render, crea un **Web Service** (New → Web Service) apuntando a
   tu repo.
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
     (o deja que Render use el `Procfile` automáticamente)
3. En la pestaña **Environment** del Web Service, agrega la variable
   `DATABASE_URL` con la cadena de conexión de Supabase (paso 3 de
   arriba).
4. Despliega. Render te da una URL pública como
   `https://tu-api.onrender.com`.
5. Prueba: `https://tu-api.onrender.com/docs` debe abrir la documentación
   interactiva, y `https://tu-api.onrender.com/cv` debe regresar el JSON
   del CV. En Supabase, el **Table Editor** debería mostrar las tablas
   ya creadas con los datos que vayas agregando.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/cv` | CV completo |
| GET / PUT | `/cv/datos-personales` | Datos personales |
| GET | `/cv/experiencia` | Listar experiencia laboral |
| GET / PUT / DELETE | `/cv/experiencia/{id}` | Un registro de experiencia |
| POST | `/cv/experiencia` | Crear experiencia |
| GET | `/cv/formacion` | Listar formación académica |
| GET / PUT / DELETE | `/cv/formacion/{id}` | Un registro de formación |
| POST | `/cv/formacion` | Crear formación |
| GET | `/cv/habilidades` | Listar habilidades |
| GET / PUT / DELETE | `/cv/habilidades/{id}` | Una habilidad |
| POST | `/cv/habilidades` | Crear habilidad |

## Cómo consumir la API (ejemplos)

**Obtener el CV completo:**
```bash
curl https://tu-api.onrender.com/cv
```

**Agregar una experiencia laboral:**
```bash
curl -X POST https://tu-api.onrender.com/cv/experiencia \
  -H "Content-Type: application/json" \
  -d '{"puesto":"Desarrollador","empresa":"Acme","fecha_inicio":"2024-01","fecha_fin":"2024-06","descripcion":"..."}'
```

**Actualizar una habilidad:**
```bash
curl -X PUT https://tu-api.onrender.com/cv/habilidades/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Python","nivel":"Avanzado"}'
```

**Eliminar un registro de formación:**
```bash
curl -X DELETE https://tu-api.onrender.com/cv/formacion/1
```

También puedes importar `https://tu-api.onrender.com/openapi.json` en
Postman para generar automáticamente una colección con todos los
endpoints.
