from fastapi import APIRouter, Depends, HTTPException, status, Response, Request

from app.config import settings
from app.models.user import User
from app.dependencies import get_auth_service, get_current_user, verify_admin_key
from app.schemas.auth import AccessTokenDTO, UserLoginDTO, UserDTO, UserRegisterDTO
from app.services.auth_service import (
    AuthService,
    UserAlreadyExistsError,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AccessTokenDTO)
async def login_controller(
    response: Response,
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

    data = {"sub": str(user.id)}
    access_token = service.create_access_token(data)
    refresh_token = await service.create_refresh_token(data)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.refresh_token_lifespan * 60,
        samesite="lax",
        secure=False
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    refresh_token = request.cookies.get("refresh_token")
    response.delete_cookie("refresh_token")

    await service.delete_refresh_token(refresh_token)


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


@router.post("/refresh", response_model=AccessTokenDTO)
async def refresh_access_token_controller(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    validated = await service.verify_refresh_token(token=refresh_token)
    if not validated:
        await service.delete_refresh_token(refresh_token)
        response.delete_cookie("refresh_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await service.get_current_user(refresh_token)

    access_token = service.create_access_token(
        data={"sub": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "Bearer"}
