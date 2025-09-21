from pydantic import BaseModel
from typing import Optional

# --- 페이지 데이터의 기본 형태 ---
# 생성과 수정 시 공통으로 사용될 필드들을 정의합니다.
class PageBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# --- 페이지 생성을 위한 스키마 ---
# API를 통해 페이지를 생성할 때 받아들일 데이터의 형태입니다.
class PageCreate(PageBase):
    slug: str
    title: str
    content: str

# --- 페이지 수정을 위한 스키마 ---
# PageBase를 상속받아 모든 필드를 선택적으로 만들어 부분 수정이 가능하도록 합니다.
class PageUpdate(PageBase):
    pass

# --- API 응답을 위한 최종 스키마 ---
# 클라이언트에게 최종적으로 보여줄 데이터의 형태입니다.
class Page(BaseModel):
    slug: str
    title: str
    content: str

    class Config:
        from_attributes = True # SQLAlchemy 모델 객체를 Pydantic 모델로 변환 가능하게 함

