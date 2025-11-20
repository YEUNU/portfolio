from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.v1 import deps
from app.crud import crud_board

router = APIRouter()

@router.get("/sitemap.xml", response_class=PlainTextResponse)
def generate_sitemap(db: Session = Depends(deps.get_db)):
    """
    검색 엔진을 위한 sitemap.xml을 동적으로 생성합니다.
    """
    base_url = "https://portfolio.ywsung.ai.kr"  # 실제 도메인으로 변경 필요
    
    # 기본 페이지들
    urls = [
        f'  <url><loc>{base_url}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>',
        f'  <url><loc>{base_url}/about</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>',
        f'  <url><loc>{base_url}/contact</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>',
    ]
    
    # 모든 포트폴리오 게시글 추가 (고정 페이지 제외)
    posts = crud_board.board.get_multi_posts_only(db, limit=1000)
    for post in posts:
        last_modified = post.updated_at or post.created_at
        urls.append(
            f'  <url><loc>{base_url}/post/{post.id}</loc>'
            f'<lastmod>{last_modified.strftime("%Y-%m-%d")}</lastmod>'
            f'<changefreq>weekly</changefreq><priority>0.9</priority></url>'
        )
    
    # 태그별 페이지 추가
    tags = crud_board.board.get_all_tags(db)
    for tag in tags:
        urls.append(
            f'  <url><loc>{base_url}/?tag={tag}</loc>'
            f'<changefreq>weekly</changefreq><priority>0.7</priority></url>'
        )
    
    sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''
    
    return sitemap_content