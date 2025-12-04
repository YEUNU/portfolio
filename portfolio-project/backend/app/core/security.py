from datetime import datetime, timedelta, timezone
from typing import Any, Union
import secrets as py_secrets

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# --- [수정된 부분 시작] ---

# 1. 새로운 기본 알고리즘으로 argon2를 지정합니다.
# 2. bcrypt는 기존 비밀번호 검증을 위해 남겨둡니다 (deprecated="auto").
#    이렇게 하면 passlib이 알아서 기존 bcrypt 해시를 인식하고 검증해줍니다.
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# --- [수정된 부분 끝] ---

ALGORITHM = "HS256"

# JWT 발급자 및 대상 식별자 (토큰 위조 방지를 위한 추가 클레임)
JWT_ISSUER = "portfolio-api"
JWT_AUDIENCE = "portfolio-frontend"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    주어진 subject(보통 사용자 ID)를 기반으로 JWT 액세스 토큰을 생성합니다.
    
    보안 강화:
    - jti (JWT ID): 각 토큰에 고유 식별자 부여
    - iss (Issuer): 토큰 발급자 식별
    - aud (Audience): 토큰 대상 식별
    - iat (Issued At): 토큰 발급 시간
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 설정 파일에서 지정한 만료 시간(분)을 사용
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    now = datetime.now(timezone.utc)
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": now,
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "jti": py_secrets.token_hex(16),  # 고유 토큰 ID
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    입력된 일반 비밀번호와 해시된 비밀번호를 비교하여 일치 여부를 반환합니다.
    (Argon2로 변경하여 더 이상 72바이트 제한이 없으므로 잘라내는 로직을 제거합니다.)
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    일반 비밀번호를 받아 새로운 기본 알고리즘(argon2)의 해시 값을 생성합니다.
    (Argon2로 변경하여 더 이상 72바이트 제한이 없으므로 잘라내는 로직을 제거합니다.)
    """
    return pwd_context.hash(password)

