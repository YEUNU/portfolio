from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

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
    모든 게시글을 조회하거나, 태그를 기준으로 필터링하여 조회합니다.
    - tags (쿼리 파라미터): "fastapi,python" 과 같은 형태로 전달하면 해당 태그를 포함하는 게시글을 필터링합니다.
    """
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        posts = crud_board.board.get_multi_by_tags(db, tags=tag_list, skip=skip, limit=limit)
    else:
        posts = crud_board.board.get_multi(db, skip=skip, limit=limit)
    return posts

@router.get("/tags", response_model=List[str])
def get_all_tags(db: Session = Depends(deps.get_db)):
    """
    데이터베이스에 저장된 모든 유니크한 태그 목록을 조회합니다.
    프론트엔드 사이드바의 태그 필터 목록을 구성하는 데 사용됩니다.
    """
    return crud_board.board.get_all_tags(db)


@router.post("/", response_model=schemas.Board, status_code=status.HTTP_201_CREATED)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: schemas.BoardCreate,
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    새로운 게시글을 생성합니다. (관리자 권한 필요)
    JWT 토큰을 통해 인증된 관리자만 이 API를 사용할 수 있습니다.
    """
    post = crud_board.board.create_with_owner(db=db, obj_in=post_in, owner_id=current_user.id)
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
    post_id: int,
    post_in: schemas.BoardUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    기존 게시글을 수정합니다. (관리자 권한 필요)
    """
    post = crud_board.board.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = crud_board.board.update(db=db, db_obj=post, obj_in=post_in)
    return post


@router.delete("/{post_id}", response_model=schemas.Board)
def delete_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    게시글을 삭제합니다. (관리자 권한 필요)
    """
    post = crud_board.board.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = crud_board.board.remove(db=db, id=post_id)
    return post

