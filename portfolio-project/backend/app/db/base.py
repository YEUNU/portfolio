from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any

@as_declarative()
class Base:
    """모든 SQLAlchemy 모델이 상속받는 기본 클래스입니다."""
    id: Any
    __name__: str

    # 모든 테이블에 __tablename__을 자동으로 생성해주는 데코레이터입니다.
    # 예: Board 클래스 -> "board" 테이블
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

