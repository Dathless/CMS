from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token as create_jwt_refresh_token,
    decode_token,
)
from app.crud.user import get_user_by_username
from app.crud.refresh_token import (
    create_refresh_token,
    get_refresh_token,
    delete_refresh_token,
)
from app.schemas.auth import Token, TokenRefresh, LoginRequest
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, request.username)
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(subject=user.username)
    refresh_token = create_jwt_refresh_token(subject=user.username)

    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    create_refresh_token(db, user.id, refresh_token, expires_at)

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
def refresh_token(body: TokenRefresh, db: Session = Depends(get_db)):
    try:
        payload = decode_token(body.refresh_token)
        username = payload.get("sub")
        token_type = payload.get("type")
        if username is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    db_token = get_refresh_token(db, body.refresh_token)
    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token not found or revoked")

    delete_refresh_token(db, body.refresh_token)

    new_access = create_access_token(subject=username)
    new_refresh = create_jwt_refresh_token(subject=username)

    user = get_user_by_username(db, username)
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    create_refresh_token(db, user.id, new_refresh, expires_at)

    return Token(access_token=new_access, refresh_token=new_refresh)


@router.post("/logout")
def logout(body: TokenRefresh, db: Session = Depends(get_db)):
    delete_refresh_token(db, body.refresh_token)
    return {"message": "Logged out successfully"}
