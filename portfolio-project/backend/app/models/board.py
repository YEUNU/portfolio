from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

# 프로젝트의 Base 클래스 경로에 맞게 import 합니다.
# 이전 컨텍스트에 따라 app.db.base_class.py 로 가정합니다.
from app.db.base import Base


class Board(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    content = Column(Text, nullable=False)
    
    # --- [핵심] About/Contact 페이지를 위한 slug 컬럼 유지 ---
    # 이 컬럼이 없으면 고정 페이지 수정/삭제 시 에러가 발생합니다.
    slug = Column(String(50), unique=True, index=True, nullable=True)

    # --- 태그 및 소유자 정보 ---
    tags = Column(String(255), nullable=True)
    # 모든 게시글은 소유자가 있어야 하므로 nullable=False를 유지하는 것이 좋습니다.
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    # --- [신규] 생성/수정 시간 자동 기록 ---
    # 데이터 관리를 위해 추가하신 created_at, updated_at 컬럼을 반영했습니다.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # --- 관계 설정 ---
    # User 모델과의 양방향 관계를 위해 back_populates를 명시하는 것이 표준적입니다.
    owner = relationship("User", back_populates="posts")

