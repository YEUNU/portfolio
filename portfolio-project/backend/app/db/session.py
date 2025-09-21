from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 데이터베이스 URL 생성
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URI

# SQLAlchemy 엔진 생성
# pool_pre_ping=True 설정은 커넥션 풀에서 연결을 가져올 때마다
# 간단한 쿼리를 실행하여 연결이 활성 상태인지 확인합니다.
# 이를 통해 DB 연결이 끊어진 경우 발생하는 오류를 방지할 수 있습니다.
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# 데이터베이스 세션 생성을 위한 SessionLocal 클래스 정의
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# API 엔드포인트에 DB 세션을 제공하는 의존성 함수
def get_db():
    """
    FastAPI 의존성 함수로, 각 요청마다 데이터베이스 세션을 생성하고,
    요청이 끝나면 세션을 닫아줍니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

