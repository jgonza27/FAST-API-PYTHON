from fastapi import APIRouter
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

router = APIRouter(
    prefix="/employees",
    responses={404: {"respuesta": "Not found"}}
)

# Obtener todos los empleados
@router.get("/")
async def index(session: SessionDep):
    employees = await getAllEmployees(session)
    return {"respuesta": employees}

# Obtener un empleado por su DNI
@router.get("/{DNI}")
async def show(DNI: str, session: SessionDep):
    employeeFound = await getOneEmployeeByDNI(session, DNI)
    if employeeFound is not None:
        return {"respuesta": employeeFound}
    return {"respuesta": f"Empleado con DNI {DNI} no encontrado"}

# Crear un nuevo empleado
@router.post("/")
async def store(employee: Employee, session: SessionDep):
    # Verificar si ya existe un empleado con ese login
    if await getOneEmployeeByLogin(session, employee.login) is not None:
        return {"respuesta": f"El empleado con login '{employee.login}' ya existe"}

    await insertOneEmployee(employee, session)
    return {"respuesta": f"Empleado creado con login '{employee.login}'"}

# Actualizar un empleado por su DNI
@router.put("/{DNI}")
async def update(DNI: str, session: SessionDep, employee: Employee):
    actualizadoOK = await updateOneEmployeeByDNI(employee, session, DNI)
    if actualizadoOK:
        return {"respuesta": "Empleado actualizado correctamente"}
    return {"respuesta": f"Empleado con DNI {DNI} no encontrado"}

# Eliminar un empleado por su DNI
@router.delete("/{DNI}")
async def destroy(DNI: str, session: SessionDep):
    borradoOK = await deleteOneEmployeeByDNI(session, DNI)
    if borradoOK:
        return {"respuesta": "Empleado eliminado correctamente"}
    return {"respuesta": f"Empleado con DNI {DNI} no encontrado"}
