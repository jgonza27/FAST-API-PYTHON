from .authModel import UserInDB, TokenData, User
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from utils.db import SessionDep
from sqlmodel import select
from employees.employeesModel import Employee
from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv

# ==========================================================
# 🌱 CARGAR VARIABLES DESDE .env
# ==========================================================
load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ==========================================================
# 🔐 CONFIGURACIÓN DE AUTENTICACIÓN
# ==========================================================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==========================================================
# 🧩 FUNCIONES AUXILIARES
# ==========================================================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)


def get_user(session: SessionDep, login: str):
    """Obtiene un empleado desde la base de datos por su login."""
    statement = select(Employee).where(Employee.login == login)
    result = session.exec(statement).first()
    if result is not None:
        return UserInDB(
            login=result.login,
            password=result.password,
            DNI=result.DNI,
            name=result.name,
            department_id=result.department_id,
        )
    return None


def authenticate_user(session: SessionDep, login: str, password: str):
    """Verifica las credenciales: login y contraseña (bcrypt)."""
    user = get_user(session, login)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Crea un token JWT con expiración."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ==========================================================
# 👥 DEPENDENCIAS DE AUTORIZACIÓN
# ==========================================================
async def get_current_user(
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    """Decodifica el token JWT y obtiene el usuario autenticado."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
        token_data = TokenData(login=login)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(session, token_data.login)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Devuelve el usuario actual autenticado (activo)."""
    return current_user
