from utils.db import SessionDep
from .employeesModel import Employee
from sqlmodel import select
from passlib.context import CryptContext

# ==========================================================
# 🔐 CONFIGURACIÓN DE HASH DE CONTRASEÑAS
# ==========================================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Genera el hash seguro de una contraseña."""
    return pwd_context.hash(password)

# ==========================================================
# 📋 CRUD DE EMPLEADOS
# ==========================================================

async def getAllEmployees(session: SessionDep):
    """Obtiene todos los empleados."""
    statement = select(Employee)
    result = session.exec(statement).all()
    return result


async def getOneEmployeeByDNI(session: SessionDep, DNI: str):
    """Obtiene un empleado por su DNI."""
    statement = select(Employee).where(Employee.DNI == DNI)
    employeeFound = session.exec(statement).first()
    return employeeFound


async def getOneEmployeeByLogin(session: SessionDep, login: str):
    """Obtiene un empleado por su login."""
    statement = select(Employee).where(Employee.login == login)
    result = session.exec(statement).first()
    return result


async def insertOneEmployee(employee: Employee, session: SessionDep):
    """Inserta un nuevo empleado (con contraseña hasheada)."""
    # Hashear la contraseña antes de guardar
    employee.password = get_password_hash(employee.password)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


async def deleteOneEmployeeByDNI(session: SessionDep, DNI: str):
    """Elimina un empleado por su DNI."""
    employeeFound = session.get(Employee, DNI)
    if employeeFound is None:
        return False
    session.delete(employeeFound)
    session.commit()
    return True


async def updateOneEmployeeByDNI(employee: Employee, session: SessionDep, DNI: str):
    """Actualiza los datos de un empleado (re-hasheando la contraseña si cambia)."""
    statement = select(Employee).where(Employee.DNI == DNI)
    employeeFound = session.exec(statement).first()

    if employeeFound is None:
        return False

    # ⚠️ No se modifica el DNI (clave primaria)
    employeeFound.name = employee.name
    employeeFound.login = employee.login

    # Re-hashear contraseña si se actualiza
    if employee.password:
        employeeFound.password = get_password_hash(employee.password)

    employeeFound.department_id = employee.department_id

    session.add(employeeFound)
    session.commit()
    session.refresh(employeeFound)
    return True
