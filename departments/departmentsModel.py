from pydantic import BaseModel

class Department(BaseModel):
    id: int
    name: str
    phone: str | None = None
    email: str | None = None

class DepartmentList(BaseModel):
    departments: list[Department]
