from fastapi import APIRouter
from departments.departmentsService import (
    getAllDepartments,
    getOneDepartmentByID,
    getOneDepartmentByName,
    insertOneDepartment,
)
from utils.db import SessionDep
from .departmentsModel import Department, DepartmentList

router = APIRouter(
    prefix="/departments",
    responses={404: {"respuesta": "Not found"}}
)

storageDepartment = DepartmentList(departments=[])


@router.get("/")
async def index(session: SessionDep):
    departments = await getAllDepartments(session)
    return {"departments": departments}


@router.get("/{id}")
async def show(id: int, session: SessionDep):
    departmentFound = await getOneDepartmentByID(session, id)
    if departmentFound is not None:
        return {"respuesta": departmentFound}
    return {"respuesta": f"Departamento con id {id} no encontrado"}


@router.post("/")
async def store(department: Department, session: SessionDep):
    # Verificar si ya existe un departamento con el mismo nombre
    existing = await getOneDepartmentByName(session, department.name)
    if existing is not None:
        return {"respuesta": f"El Departamento con nombre '{department.name}' ya existe"}

    # Insertar nuevo registro
    new_department = await insertOneDepartment(department, session)
    return {"respuesta": f"Departamento '{new_department.name}' creado exitosamente"}


@router.put("/{id}")
async def update(id: int, department: Department, session: SessionDep):
    existing = await getOneDepartmentByID(session, id)
    if existing is None:
        return {"respuesta": f"No existe el departamento con id {id}"}

    existing.name = department.name
    existing.phone = department.phone
    existing.email = department.email
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return {"respuesta": f"Departamento {id} actualizado correctamente"}


@router.delete("/{id}")
async def destroy(id: int, session: SessionDep):
    department = await getOneDepartmentByID(session, id)
    if not department:
        return {"respuesta": f"No se encontró el departamento con id {id}"}

    session.delete(department)
    session.commit()
    return {"respuesta": f"Departamento con id {id} eliminado correctamente"}
