from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.crud import crud_user

# OAuth2PasswordBearer는 "/api/v1/login" 엔드포인트에서 토큰을 가져오는 의존성입니다.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    """
    API 요청 헤더의 JWT 토큰을 검증하고, 해당 토큰의 사용자 정보를 반환합니다.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # 토큰에서 추출한 사용자 ID를 사용하여 DB에서 사용자 정보를 조회합니다.
    user = crud_user.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_admin_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    현재 로그인한 사용자가 활성 상태이고 관리자인지 확인합니다.
    관리자가 아닐 경우, 403 Forbidden 에러를 발생시킵니다.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
