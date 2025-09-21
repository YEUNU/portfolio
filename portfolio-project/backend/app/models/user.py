from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class User(Base):
    """사용자 정보 저장을 위한 데이터베이스 모델입니다."""
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean(), default=False)

