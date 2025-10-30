from pydantic import BaseModel

# Modelo para el token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

# Información que se extrae del token
class TokenData(BaseModel):
    login: str | None = None

# Modelo base de usuario (sin contraseña)
class User(BaseModel):
    login: str
    DNI: str | None = None
    name: str | None = None
    department_id: int | None = None

# Modelo de usuario almacenado en base de datos (con contraseña)
class UserInDB(User):
    password: str
