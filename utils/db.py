from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("mysql+pymysql://root:password123@mariadb/restfastapi", echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
