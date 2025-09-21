from fastapi import APIRouter

from app.api.v1.endpoints import login, board, page, upload # ✅ upload 라우터 import 추가

api_router = APIRouter()

# 기존 라우터들
api_router.include_router(login.router, prefix="/login", tags=["auth"])
api_router.include_router(board.router, prefix="/board", tags=["board"])
api_router.include_router(page.router, prefix="/pages", tags=["pages"])

# ✅ 추가된 라우터: /api/v1/upload 경로로 들어오는 요청들을 upload.py가 처리하도록 포함
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])

