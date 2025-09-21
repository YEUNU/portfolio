from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base

class Board(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    
    # --- 기능 추가 및 개선 ---
    # 1. 해시태그 필드 추가 (쉼표로 구분된 문자열)
    tags = Column(String, nullable=True) 
    
    # 2. 기존 author 필드를 User 모델과 연결되는 외래 키로 대체
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # --- 기존 필드 유지 ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # --- 관계 설정 ---
    owner = relationship("User")

