from utils.db import SessionDep
from .departmentsModel import Department
from sqlmodel import select


async def getAllDepartments(session: SessionDep):
    statement = select(Department)
    result = session.exec(statement).all()
    return result


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
