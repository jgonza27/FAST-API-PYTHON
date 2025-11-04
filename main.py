from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from auth import authController
from departments import departmentsController
from employees import employeesController
from utils.db import create_db_and_tables

# ==========================================================
# 🌍 Configuración inicial
# ==========================================================

# Carga de variables de entorno (.env)
load_dotenv()

# Inicialización de la app
app = FastAPI(
    title="REST API con FastAPI",
    description="API REST completa con autenticación JWT, manejo de empleados y departamentos.",
    version="1.0.0"
)

# ==========================================================
# ⚙️ Middleware CORS
# ==========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Cambia "*" por dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# 🌐 Endpoints base
# ==========================================================
@app.get("/")
async def root():
    """Ruta principal de verificación del servicio."""
    return {"message": "🚀 API REST creada con FASTAPI y autenticación JWT"}

# ==========================================================
# 📦 Rutas (Controladores)
# ==========================================================
app.include_router(departmentsController.router, prefix="/api")
app.include_router(employeesController.router, prefix="/api")
app.include_router(authController.router, prefix="/api")

# ==========================================================
# 🗄️ Creación de tablas al iniciar
# ==========================================================
@app.on_event("startup")
def on_startup():
    """Se ejecuta al iniciar la aplicación: crea tablas en la BD."""
    create_db_and_tables()
