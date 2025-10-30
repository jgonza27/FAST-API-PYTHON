from fastapi import APIRouter
from utils.db import SessionDep
from .departmentsModel import Department, DepartmentList
from .departmentsService import (
    getAllDepartments,
    getOneDepartmentByID,
    insertOneDepartment,
    deleteOneDepartmentByID,
    updateOneDepartmentByID,
)

router = APIRouter(
    prefix="/departments",
    responses={404: {"respuesta": "Not found"}}
)

storageDepartment = DepartmentList(departments=[])

@router.get("/")
async def index(session: SessionDep):
    return await getAllDepartments(session)

@router.get("/{id}")
async def show(id: int, session: SessionDep):
    department = await getOneDepartmentByID(session, id)
    if department is None:
        return {"respuesta": f"Departamento con id {id} no encontrado"}
    return department

@router.post("/")
async def store(department: Department, session: SessionDep):
    return await insertOneDepartment(department, session)

@router.put("/{id}")
async def update(id: int, session: SessionDep, department: Department):
    actualizadoOK = await updateOneDepartmentByID(department, session, id)
    if actualizadoOK:
        return {"respuesta": "Actualizado el departamento"}
    return {"respuesta": f"Departamento con id {id} no encontrado"}

@router.delete("/{id}")
async def destroy(id: int, session: SessionDep):
    borradoOK = await deleteOneDepartmentByID(session, id)
    if borradoOK:
        return {"respuesta": "Borrado el departamento"}
    return {"respuesta": f"Departamento con id {id} no encontrado"}
