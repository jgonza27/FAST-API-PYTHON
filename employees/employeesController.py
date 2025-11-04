from fastapi import APIRouter, Depends
from employees.employeesService import (
    deleteOneEmployeeByDNI,
    getAllEmployees,
    getOneEmployeeByDNI,
    getOneEmployeeByLogin,
    insertOneEmployee,
    updateOneEmployeeByDNI,
)
from utils.db import SessionDep
from .employeesModel import Employee
from auth.authModel import User
from typing import Annotated
from auth.authService import get_current_active_user

# ==========================================================
# 📦 Configuración del router
# ==========================================================
router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
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
    🧾 Obtiene todos los empleados (solo usuarios autenticados).
    """
    employees = await getAllEmployees(session)
    return {"respuesta": employees}


@router.get("/{DNI}")
async def show(
    DNI: str,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    🔍 Obtiene un empleado por su DNI.
    """
    employee = await getOneEmployeeByDNI(session, DNI)
    if not employee:
        return {"respuesta": f"Empleado con DNI {DNI} no encontrado"}
    return {"respuesta": employee}


@router.post("/")
async def store(
    employee: Employee,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    ➕ Crea un nuevo empleado.
    Se valida el login para evitar duplicados.
    """
    existing_employee = await getOneEmployeeByLogin(session, employee.login)
    if existing_employee:
        return {"respuesta": f"El empleado con login '{employee.login}' ya existe"}

    await insertOneEmployee(employee, session)
    return {"respuesta": f"Empleado '{employee.name}' creado correctamente"}


@router.put("/{DNI}")
async def update(
    DNI: str,
    employee: Employee,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    ✏️ Actualiza los datos de un empleado.
    """
    actualizadoOK = await updateOneEmployeeByDNI(employee, session, DNI)
    if not actualizadoOK:
        return {"respuesta": f"Empleado con DNI {DNI} no encontrado"}
    return {"respuesta": f"Empleado con DNI {DNI} actualizado correctamente"}


@router.delete("/{DNI}")
async def destroy(
    DNI: str,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    ❌ Elimina un empleado por su DNI.
    """
    borradoOK = await deleteOneEmployeeByDNI(session, DNI)
    if not borradoOK:
        return {"respuesta": f"Empleado con DNI {DNI} no encontrado"}
    return {"respuesta": f"Empleado con DNI {DNI} eliminado correctamente"}
