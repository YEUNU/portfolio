from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # ✅ StaticFiles import 추가
import logging

from app.api.v1.api_router import api_router
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db import base
from app.initial_data import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 인스턴스 먼저 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# ✅ 추가: '/static' 경로로 들어오는 요청을 'app/static' 디렉터리로 연결
# 이 설정을 통해 업로드된 이미지에 브라우저가 접근할 수 있게 됩니다.
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# FastAPI 시작 이벤트 핸들러
@app.on_event("startup")
def on_startup():
    logger.info("애플리케이션 시작 이벤트를 실행합니다...")
    try:
        db = SessionLocal()
        # 애플리케이션 시작 시 데이터베이스 테이블 생성은 개발용 옵션으로 제한
        if settings.INIT_DB:
            base.Base.metadata.create_all(bind=engine)
        # 초기 데이터 확인 및 생성 (초기 관리자 계정 등)
        init_db(db)
    finally:
        db.close()
    logger.info("초기 데이터 확인 및 생성이 완료되었습니다.")

# CORS 미들웨어 설정
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# API 라우터 포함
app.include_router(api_router, prefix=settings.API_V1_STR)

