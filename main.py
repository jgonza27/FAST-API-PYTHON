from fastapi import FastAPI
from dotenv import load_dotenv

# ==========================================================
# 🌱 CARGA GLOBAL DE VARIABLES DE ENTORNO
# ==========================================================
load_dotenv()  # Lee .env y las guarda en os.environ

# ==========================================================
# 🚀 IMPORTACIONES DE CONTROLADORES
# ==========================================================
from auth import authController
from departments import departmentsController
from employees import employeesController
from utils.db import create_db_and_tables

# ==========================================================
# ⚙️ CONFIGURACIÓN DE LA APLICACIÓN FASTAPI
# ==========================================================
app = FastAPI(title="API REST con FastAPI")

@app.get("/")
async def root():
    return {"message": "API Rest creada con FASTAPI"}

# ==========================================================
# 🧭 REGISTRO DE ROUTERS
# ==========================================================
app.include_router(departmentsController.router, prefix="/api")
app.include_router(employeesController.router, prefix="/api")
app.include_router(authController.router, prefix="/api")

# ==========================================================
# ⚙️ EVENTOS DE INICIO
# ==========================================================
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
