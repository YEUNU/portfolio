from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# 비밀번호 해싱을 위한 CryptContext 객체 생성 (bcrypt 알고리즘 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    주어진 subject(보통 사용자 ID)를 기반으로 JWT 액세스 토큰을 생성합니다.
    (이 함수는 수정이 필요 없습니다.)
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 설정 파일에서 지정한 만료 시간(분)을 사용
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    입력된 일반 비밀번호와 해시된 비밀번호를 비교하여 일치 여부를 반환합니다.
    """
    # bcrypt의 72바이트 제한에 맞춰 비밀번호를 자릅니다.
    truncated_password = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(truncated_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    일반 비밀번호를 받아 bcrypt 해시 값을 생성하여 반환합니다.
    """
    # bcrypt의 72바이트 제한에 맞춰 비밀번호를 자릅니다.
    truncated_password = password.encode('utf-8')[:72]
    return pwd_context.hash(truncated_password)