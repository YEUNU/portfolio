from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- 게시글 데이터의 기본 형태 ---
# 생성과 수정 시 공통으로 사용될 필드들을 정의합니다.
class BoardBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None

# --- 게시글 생성을 위한 스키마 ---
# API를 통해 게시글을 생성할 때 받아들일 데이터의 형태입니다.
# BoardBase를 상속받고, title과 content는 필수 항목으로 지정합니다.
class BoardCreate(BoardBase):
    title: str
    content: str

# --- 게시글 수정을 위한 스키마 ---
# BoardBase를 상속받아 모든 필드를 선택적으로 만들어 부분 수정이 가능하도록 합니다.
class BoardUpdate(BoardBase):
    pass

# --- API 응답을 위한 최종 스키마 ---
# 클라이언트에게 최종적으로 보여줄 데이터의 형태입니다.
# 데이터베이스 모델의 필드들을 포함합니다.
class Board(BaseModel):
    id: int
    title: str
    content: str
    tags: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True # SQLAlchemy 모델 객체를 Pydantic 모델로 변환 가능하게 함

