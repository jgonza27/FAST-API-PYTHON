from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API Rest creada con FASTAPI"}

from departments import departmentsController
app.include_router(departmentsController.router, prefix="/api")

from departments.departmentsModel import create_db_and_tables

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
