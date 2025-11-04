from fastapi import APIRouter, Depends
from departments.departmentsService import (
    deleteOneDepartmentByID,
    getAllDepartments,
    getOneDepartmentByID,
    getOneDepartmentByName,
    insertOneDepartment,
    updateOneDepartmentByID,
)
from utils.db import SessionDep
from .departmentsModel import Department, DepartmentList
from auth.authModel import User
from typing import Annotated
from auth.authService import get_current_active_user

# ==========================================================
# 📦 Configuración del router
# ==========================================================
router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
    responses={404: {"respuesta": "Not found"}},
)

# ==========================================================
# 🔒 Endpoints protegidos con JWT
# ==========================================================

@router.get("/")
async def index(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    🧾 Obtener todos los departamentos.
    Solo accesible para usuarios autenticados.
    """
    departments = await getAllDepartments(session)
    return {"respuesta": departments}


@router.get("/{id}")
async def show(
    id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    🔍 Obtener un departamento por ID.
    """
    departmentFound = await getOneDepartmentByID(session, id)
    if not departmentFound:
        return {"respuesta": f"Departamento con id {id} no encontrado"}
    return {"respuesta": departmentFound}


@router.post("/")
async def store(
    department: Department,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    ➕ Crear un nuevo departamento.
    """
    await insertOneDepartment(department, session)
    return {"respuesta": f"Departamento '{department.name}' creado correctamente"}


@router.put("/{id}")
async def update(
    id: int,
    session: SessionDep,
    department: Department,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    ✏️ Actualizar un departamento existente.
    """
    actualizadoOK = await updateOneDepartmentByID(department, session, id)
    if not actualizadoOK:
        return {"respuesta": f"Departamento con id {id} no encontrado"}
    return {"respuesta": f"Departamento con id {id} actualizado correctamente"}


@router.delete("/{id}")
async def destroy(
    id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    ❌ Eliminar un departamento por su ID.
    """
    borradoOK = await deleteOneDepartmentByID(session, id)
    if not borradoOK:
        return {"respuesta": f"Departamento con id {id} no encontrado"}
    return {"respuesta": f"Departamento con id {id} eliminado correctamente"}
