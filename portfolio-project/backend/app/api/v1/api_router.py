from fastapi import APIRouter

from app.api.v1.endpoints import login, board, upload, sitemap

api_router = APIRouter()

# 인증 라우터
api_router.include_router(login.router, prefix="/login", tags=["auth"])

# 게시글 라우터 (일반 포스트 + 고정 페이지)
api_router.include_router(board.router, prefix="/board", tags=["board"])

# 파일 업로드 라우터
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])

# SEO sitemap 라우터
api_router.include_router(sitemap.router, tags=["seo"])

