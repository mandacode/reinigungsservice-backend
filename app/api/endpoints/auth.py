from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.models.user import User
from app.dependencies import get_auth_service, get_current_user, verify_admin_key
from app.schemas.auth import TokenDTO, UserLoginDTO, UserDTO, UserRegisterDTO
from app.services.auth_service import (
    TokenIsBlacklistedError,
    AuthService,
    UserAlreadyExistsError,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenDTO)
async def create_access_token_controller(
    creds: UserLoginDTO,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.authenticate(creds.username, creds.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = service.create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "username": user.username,
    }


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    service: AuthService = Depends(get_auth_service),
    _=Depends(get_current_user),
):
    token = credentials.credentials

    try:
        user = await service.get_current_user(token=token)
    except TokenIsBlacklistedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is blacklisted",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        await service.blacklist_token(token=token, user_id=user.id)
        return {"message": "Successfully logged out"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/me", response_model=UserDTO)
async def get_current_user_info_controller(user: User = Depends(get_current_user)):
    return user


@router.post("/register")
async def register_admin_user_controller(
    data: UserRegisterDTO,
    _=Depends(verify_admin_key),
    service: AuthService = Depends(get_auth_service),
):
    try:
        await service.register_user(username=data.username, password=data.password)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"status": "ok", "message": "User created"}
