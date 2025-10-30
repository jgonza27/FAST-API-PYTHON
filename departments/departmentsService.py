from utils.db import SessionDep
from .departmentsModel import Department
from sqlmodel import select

async def getAllDepartments(session: SessionDep):
    statement = select(Department)
    results = session.exec(statement)
    return results.all()

async def getOneDepartmentByID(session: SessionDep, id: int):
    return session.get(Department, id)

async def getOneDepartmentByName(session: SessionDep, name: str):
    statement = select(Department).where(Department.name == name)
    result = session.exec(statement).first()
    return result

async def insertOneDepartment(department: Department, session: SessionDep):
    session.add(department)
    session.commit()
    session.refresh(department)
    return department

async def deleteOneDepartmentByID(session: SessionDep, id: int):
    departmentFound = session.get(Department, id)
    if departmentFound is None:
        return False
    session.delete(departmentFound)
    session.commit()
    return True

async def updateOneDepartmentByID(department: Department, session: SessionDep, id: int):
    # Buscar el departamento por ID
    statement = select(Department).where(Department.id == id)
    departmentFound = session.exec(statement).first()

    if departmentFound is None:
        return False

    # Actualizar campos
    departmentFound.name = department.name
    departmentFound.phone = department.phone
    departmentFound.email = department.email

    session.add(departmentFound)
    session.commit()
    session.refresh(departmentFound)
    return True
