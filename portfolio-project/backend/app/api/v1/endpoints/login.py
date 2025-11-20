from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, models
from app.api.v1 import deps
from app.core import security
from app.core.config import settings
from app.crud import crud_user

router = APIRouter()

@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 호환 폼 데이터로 액세스 토큰을 발급받습니다.
    
    사용자 이름(username)과 비밀번호(password)를 받아 인증을 수행하고,
    성공 시 JWT 토큰을 반환합니다.
    관리자의 경우 더 짧은 세션 타임아웃이 적용됩니다.
    """
    user = crud_user.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    # 관리자의 경우 더 짧은 만료 시간 적용
    if user.is_admin:
        access_token_expires = timedelta(minutes=settings.ADMIN_SESSION_TIMEOUT_MINUTES)
    else:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": access_token_expires.total_seconds(),  # 만료 시간을 초 단위로 반환
    }

@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)):
    """
    테스트용 엔드포인트: 현재 로그인된 사용자의 정보를 반환합니다.
    프론트엔드에서 토큰의 유효성을 확인할 때 유용하게 사용할 수 있습니다.
    """
    return current_user

@router.post("/refresh-token", response_model=schemas.Token)
def refresh_token(current_user: models.User = Depends(deps.get_current_user)):
    """
    현재 토큰을 사용하여 새로운 토큰을 발급받습니다.
    관리자의 경우 더 짧은 세션 타임아웃이 적용됩니다.
    """
    # 관리자의 경우 더 짧은 만료 시간 적용
    if current_user.is_admin:
        access_token_expires = timedelta(minutes=settings.ADMIN_SESSION_TIMEOUT_MINUTES)
    else:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = security.create_access_token(
        current_user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": access_token_expires.total_seconds(),
    }

