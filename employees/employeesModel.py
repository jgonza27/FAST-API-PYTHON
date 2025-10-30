from sqlmodel import Field, SQLModel

class Employee(SQLModel, table=True):
    DNI: str = Field(primary_key=True)
    name: str | None = None
    login: str | None = Field(default=None, index=True)
    password: str | None = None
    department_id: int | None = Field(default=None, foreign_key="department.id")
