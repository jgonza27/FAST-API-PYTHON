from fastapi import FastAPI
from departments import departmentsController

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API Rest creada con FASTAPI"}

app.include_router(departmentsController.router, prefix="/api")
