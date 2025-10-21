from fastapi import APIRouter
from .departmentsModel import Department, DepartmentList

router = APIRouter(
    prefix="/departments",
    responses={404: {"respuesta": "Not found"}}
)

# "Base de datos" temporal en memoria
storageDepartment = DepartmentList(departments=[])

# Obtener todos los departamentos
@router.get("/")
async def index():
    return {"respuesta": storageDepartment.departments}

# Obtener un departamento por id
@router.get("/{id}")
async def show(id: int):
    for item in storageDepartment.departments:
        if item.id == id:
            return {"respuesta": item}
    return {"respuesta": f"Departamento con id {id} no encontrado"}

# Crear un nuevo departamento
@router.post("/")
async def store(department: Department):
    for item in storageDepartment.departments:
        if item.id == department.id:
            return {"respuesta": f"El Departamento con id {department.id} ya existe"}
        elif item.name == department.name:
            return {"respuesta": f"El Departamento con nombre {department.name} ya existe"}
    storageDepartment.departments.append(department)
    return {"respuesta": f"Creado el departamento {department.name}"}
