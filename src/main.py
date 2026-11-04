import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en sys.path para soportar 'fastapi dev src/main.py' y 'uvicorn'
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from src.database import create_db_and_tables
from src.routers import categoria_router, producto_router, proveedor_router

# Desactivar advertencia informativa de extensiones de fastapi_pagination
disable_installed_extensions_check()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de ciclo de vida de la aplicación.
    Inicializa tablas si aún no existen al iniciar la API.
    """
    create_db_and_tables()
    yield


app = FastAPI(
    title="Ferretería Industrial API - PP1 Python (EFI)",
    description="""
## Evaluación Final Integradora (EFI) - Práctica Profesionalizante 1 (Python)

Sistema de gestión comercial y catálogo para **Ferretería Industrial**, desarrollado con **FastAPI**, **SQLModel** y **SQLite**, con soporte para migraciones vía **Alembic**, paginación y esquemas anidados.

### Características del Sistema:
* **Categorías:** Clasificación de artículos (Herramientas, Pinturería, Fijaciones, etc.).
* **Proveedores:** Gestión de fabricantes y distribuidores mayoristas con validación de CUIT.
* **Productos:** Catálogo integral de artículos con claves foráneas dobles, control de stock y SKU.
* **CRUD Completo:** 5 operaciones por modelo (Create, Read All, Read One, Update, Delete).
* **Paginación:** Resultados de colecciones paginados mediante `fastapi-pagination`.
* **CORS Habilitado:** Totalmente preparado para conectar con la EFI de JavaScript.
    """,
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Equipo EFI - PP1 Python",
        "url": "https://github.com",
    },
    license_info={
        "name": "MIT License",
    },
)

# Configuración de CORS para permitir la conexión fluida con el frontend de JavaScript
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (ideal para desarrollo e integración con JS)
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, PATCH, DELETE, OPTIONS, etc.
    allow_headers=["*"],
)

# Registro de routers modulares
app.include_router(categoria_router)
app.include_router(proveedor_router)
app.include_router(producto_router)

# Configuración de paginación en la app
add_pagination(app)


@app.get(
    "/",
    tags=["General"],
    summary="Estado de la API y bienvenida",
    description="Devuelve el estado general del servicio y enlaces a la documentación interactiva.",
)
def root():
    return {
        "sistema": "Ferretería Industrial API",
        "materia": "PP1 - Python (Evaluación Final Integradora)",
        "estado": "En línea",
        "documentacion_swagger": "/docs",
        "documentacion_redoc": "/redoc",
        "modulos": [
            "/categorias",
            "/proveedores",
            "/productos",
        ],
    }
