from sqlalchemy import Column, String, Text
from app.db.base import Base

class Page(Base):
    """정적 페이지(About, Contact 등)의 콘텐츠를 저장하기 위한 모델입니다."""
    # 'about', 'contact' 등 URL로 사용될 고유 식별자
    slug = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
