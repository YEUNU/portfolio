from pydantic import BaseModel
from typing import Optional

# --- 사용자 데이터의 기본 형태 ---
# 생성과 수정 시 공통으로 사용될 필드들을 정의합니다.
class UserBase(BaseModel):
    username: Optional[str] = None
    is_admin: bool = False

# --- 사용자 생성을 위한 스키마 ---
# 관리자가 새로운 사용자를 생성할 때 받아들일 데이터의 형태입니다.
# 일반 비밀번호(password)를 받아 내부에서 해싱 처리합니다.
class UserCreate(UserBase):
    username: str
    password: str

# --- 사용자 수정을 위한 스키마 ---
# 기존 사용자의 정보를 수정할 때 사용합니다. (모든 필드는 선택적)
class UserUpdate(UserBase):
    password: Optional[str] = None

# --- API 응답을 위한 최종 스키마 ---
# 클라이언트에게 최종적으로 보여줄 데이터의 형태입니다.
# 보안을 위해 hashed_password 필드는 제외합니다.
class User(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True # SQLAlchemy 모델 객체를 Pydantic 모델로 변환 가능하게 함

