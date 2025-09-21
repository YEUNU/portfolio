from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.v1 import deps
from app.crud import crud_page

router = APIRouter()

@router.get("/{slug}", response_model=schemas.Page)
def read_page(
    slug: str,
    db: Session = Depends(deps.get_db),
):
    """
    슬러그(slug)를 기준으로 특정 페이지의 내용을 조회합니다.
    (예: /api/v1/pages/about)
    """
    page = crud_page.page.get_by_slug(db, slug=slug)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.put("/{slug}", response_model=schemas.Page)
def create_or_update_page(
    slug: str,
    *,
    db: Session = Depends(deps.get_db),
    page_in: schemas.PageUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    페이지 내용을 생성하거나 수정합니다. (관리자 권한 필요)
    해당 슬러그의 페이지가 없으면 새로 만들고, 있으면 내용을 업데이트하는 'Upsert' 방식입니다.
    """
    page = crud_page.page.get_by_slug(db, slug=slug)
    
    # 페이지가 존재하지 않으면 새로 생성
    if not page:
        # PageUpdate 스키마에는 slug가 없으므로, PageCreate 스키마로 변환하여 생성
        create_data = schemas.PageCreate(slug=slug, **page_in.model_dump())
        return crud_page.page.create(db, obj_in=create_data)
    
    # 페이지가 존재하면 내용 업데이트
    return crud_page.page.update(db, db_obj=page, obj_in=page_in)

