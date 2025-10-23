from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Annotated
from fastapi import Depends

# Modelo SQLModel
class Department(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, index=True)
    phone: str | None = None
    email: str | None = None

class DepartmentList(BaseModel):
    departments: list[Department]

# Conexión a la base de datos
engine = create_engine(
    "mysql+pymysql://root:password123@mariadb/restfastapi", 
    echo=True
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
