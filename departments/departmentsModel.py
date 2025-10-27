from pydantic import BaseModel
from sqlmodel import Field, SQLModel

# class Department(BaseModel):
#     id: int
#     name: str
#     phone: str | None = None
#     email: str | None = None
# SQLModel
class Department(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, index=True)
    phone: str | None = None
    email: str | None = None


class DepartmentList(BaseModel):
    departments: list[Department]
