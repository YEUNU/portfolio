from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base

class User(Base):
    """사용자 정보 저장을 위한 데이터베이스 모델입니다."""
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean(), default=False)

    # --- [핵심] User와 Board 모델의 양방향 관계 설정 ---
    # 이 부분이 없으면, Board 모델의 owner 관계가 짝을 찾지 못해 에러가 발생합니다.
    posts = relationship("Board", back_populates="owner")

