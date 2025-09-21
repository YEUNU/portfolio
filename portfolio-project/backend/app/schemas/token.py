from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """API가 클라이언트에게 반환하는 액세스 토큰의 형태입니다."""
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """JWT 토큰 안에 담기는 데이터(payload)의 형태입니다."""
    sub: Optional[int] = None
