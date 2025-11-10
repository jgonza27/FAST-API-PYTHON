from fastapi import FastAPI, APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
import inspect, re

# Importa tus controladores y utilidades
from auth import authController
from departments import departmentsController
from employees import employeesController
from utils.db import create_db_and_tables

# ---------------------------------------
# 🚀 Inicializa la aplicación
# ---------------------------------------
app = FastAPI(
    title="FastAPI Application",
    version="1.0.0",
    description="API REST con autenticación JWT y manejo de excepciones"
)

# Carga variables de entorno (.env)
load_dotenv()

# ---------------------------------------
# 🌍 Configuración de CORS
# ---------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# 🔐 Configuración personalizada de OpenAPI (Swagger + JWT)
# ---------------------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Añadimos un esquema de seguridad tipo Bearer Token (JWT)
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Introduce: **'Bearer <JWT>'**, donde JWT es tu token de acceso"
        }
    }

    # Analiza dinámicamente qué rutas usan jwt_required o similares
    api_routes = [route for route in app.routes if hasattr(route, "endpoint")]

    for route in api_routes:
        endpoint = route.endpoint
        path = route.path
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            try:
                source = inspect.getsource(endpoint)
                if (
                    re.search("jwt_required", source) or
                    re.search("fresh_jwt_required", source) or
                    re.search("jwt_optional", source)
                ):
                    if "paths" in openapi_schema and path in openapi_schema["paths"]:
                        if method in openapi_schema["paths"][path]:
                            openapi_schema["paths"][path][method]["security"] = [
                                {"Bearer Auth": []}
                            ]
            except (OSError, TypeError):
                # Ignora rutas internas sin código fuente accesible
                continue

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Reemplaza el generador por defecto de OpenAPI
app.openapi = custom_openapi

# ---------------------------------------
# 🌐 Rutas principales
# ---------------------------------------
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "API Rest creada con FastAPI, con JWT y manejo de excepciones"}

# Incluimos los routers de la app
app.include_router(departmentsController.router, prefix="/api")
app.include_router(employeesController.router, prefix="/api")
app.include_router(authController.router, prefix="/api")

# ---------------------------------------
# ⚠️ Manejo global de errores
# ---------------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Captura errores HTTP controlados (404, 401, etc.)
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "mensaje": exc.detail,
            "ruta": str(request.url)
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Captura errores no controlados (500)
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "mensaje": "Error interno del servidor",
            "detalle": str(exc),
            "ruta": str(request.url)
        },
    )

# ---------------------------------------
# ⚙️ Evento de inicio (creación de BD)
# ---------------------------------------
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
