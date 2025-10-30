from fastapi import APIRouter, Depends, HTTPException, status
from auth.authModel import Token, UserInDB, User
from typing import Annotated
from auth.authService import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from datetime import timedelta
from utils.db import SessionDep

router = APIRouter(prefix="/auth", responses={404: {"respuesta": "Not found"}})

# ==========================================================
# 🔑 LOGIN - Generar Token JWT usando JSON en lugar de form-data
# ==========================================================
@router.post("/token", response_model=Token)
async def login_for_access_token(session: SessionDep, user: UserInDB):
    """
    Autentica al usuario (empleado) y devuelve un token JWT.
    Recibe login y password en formato JSON, no form-data.
    """
    # Verificar usuario en base de datos
    user_db = authenticate_user(session, user.login, user.password)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token JWT con expiración
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_db.login}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


# ==========================================================
# 👤 Obtener usuario autenticado
# ==========================================================
@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    """Devuelve los datos del usuario actualmente autenticado."""
    return current_user


# ==========================================================
# 📦 Ejemplo de endpoint protegido
# ==========================================================
@router.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    """Devuelve recursos protegidos asociados al usuario autenticado."""
    return {"item_id": "Foo", "owner": current_user.login}
