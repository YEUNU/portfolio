from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Any, Union # ✅ Union, Any import 추가

from app import models, schemas
from app.api.v1 import deps
from app.crud import crud_board

router = APIRouter()

@router.get("/", response_model=List[schemas.Board])
def read_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    tags: Optional[str] = Query(None, description="쉼표로 구분된 태그들")
):
    """
    포트폴리오 게시글을 조회하거나, 태그를 기준으로 필터링하여 조회합니다.
    고정 페이지(About, Contact)는 제외됩니다.
    """
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        posts = crud_board.board.get_multi_by_tags_posts_only(db, tags=tag_list, skip=skip, limit=limit)
    else:
        posts = crud_board.board.get_multi_posts_only(db, skip=skip, limit=limit)
    return posts

@router.get("/tags", response_model=List[str])
def get_all_tags(db: Session = Depends(deps.get_db)):
    """
    데이터베이스에 저장된 모든 유니크한 태그 목록을 조회합니다.
    """
    return crud_board.board.get_all_tags(db)

@router.get("/tags/count", response_model=dict)
def get_tags_with_count(db: Session = Depends(deps.get_db)):
    """
    태그별 포스팅 개수를 포함한 태그 목록을 조회합니다.
    """
    return crud_board.board.get_tags_with_count(db)


@router.post("/", response_model=schemas.Board, status_code=status.HTTP_201_CREATED)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: schemas.BoardCreate,
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    새로운 게시글을 생성합니다. (관리자 권한 필요)
    """
    post = crud_board.board.create_with_owner(db=db, obj_in=post_in, owner_id=current_user.id)
    return post

# --- [신규 추가] Slug로 게시글을 조회하는 API 엔드포인트 ---
@router.get("/slug/{slug}", response_model=schemas.Board)
def read_post_by_slug(
    *,
    db: Session = Depends(deps.get_db),
    slug: str,
) -> Any:
    """
    고유 슬러그(slug)로 'About', 'Contact' 같은 고정 페이지를 조회합니다.
    """
    post = crud_board.board.get_by_slug(db, slug=slug)
    if not post:
        raise HTTPException(
            status_code=404, 
            detail="The post with this slug does not exist"
        )
    return post
    
@router.get("/{post_id}", response_model=schemas.Board)
def read_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
):
    """
    ID를 기준으로 특정 게시글 하나를 조회합니다.
    """
    post = crud_board.board.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=schemas.Board)
def update_post(
    *,
    db: Session = Depends(deps.get_db),
    # ✅ [수정] 숫자 ID와 문자열 slug를 모두 받을 수 있도록 변경
    post_id: Union[int, str],
    post_in: schemas.BoardUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    기존 게시글을 ID 또는 slug를 사용하여 수정합니다. (관리자 권한 필요)
    """
    # ✅ [수정] ID 또는 slug로 게시글을 가져오는 CRUD 함수 호출
    post = crud_board.board.get_by_id_or_slug(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = crud_board.board.update(db=db, db_obj=post, obj_in=post_in)
    return post


@router.delete("/{post_id}", response_model=schemas.Board)
def delete_post(
    *,
    db: Session = Depends(deps.get_db),
    # ✅ [수정] 숫자 ID와 문자열 slug를 모두 받을 수 있도록 변경
    post_id: Union[int, str],
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    게시글을 ID 또는 slug를 사용하여 삭제합니다. (관리자 권한 필요)
    """
    # ✅ [수정] ID 또는 slug로 게시글을 가져오는 CRUD 함수 호출
    post = crud_board.board.get_by_id_or_slug(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # remove 메서드는 id를 받으므로 post 객체의 id를 사용합니다.
    post = crud_board.board.remove(db=db, id=post.id)
    return post
