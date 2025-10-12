from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Union, Optional

from app.crud.base import CRUDBase
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate

class CRUDBoard(CRUDBase[Board, BoardCreate, BoardUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: BoardCreate, owner_id: int) -> Board:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_tags(self, db: Session, *, tags: List[str], skip: int = 0, limit: int = 100) -> List[Board]:
        filters = [self.model.tags.ilike(f"%{tag}%") for tag in tags]
        return db.query(self.model).filter(or_(*filters)).offset(skip).limit(limit).all()

    def get_multi_posts_only(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Board]:
        """고정 페이지(slug가 있는 게시글)를 제외하고 일반 포트폴리오 게시글만 조회합니다."""
        return db.query(self.model).filter(self.model.slug.is_(None)).offset(skip).limit(limit).all()

    def get_multi_by_tags_posts_only(self, db: Session, *, tags: List[str], skip: int = 0, limit: int = 100) -> List[Board]:
        """태그별 필터링하되, 고정 페이지는 제외하고 일반 포트폴리오 게시글만 조회합니다."""
        filters = [self.model.tags.ilike(f"%{tag}%") for tag in tags]
        return db.query(self.model).filter(or_(*filters)).filter(self.model.slug.is_(None)).offset(skip).limit(limit).all()

    def get_all_tags(self, db: Session) -> List[str]:
        # 고정 페이지를 제외하고 태그를 수집합니다.
        all_tags_tuples = db.query(self.model.tags).filter(
            self.model.tags.isnot(None),
            self.model.slug.is_(None)  # slug가 없는 일반 게시글만
        ).all()
        unique_tags = set()
        for tags_tuple in all_tags_tuples:
            tags_str = tags_tuple[0]
            if tags_str:
                tags_list = [tag.strip() for tag in tags_str.split(',')]
                unique_tags.update(tags_list)
        return sorted(list(unique_tags))

    def get_tags_with_count(self, db: Session) -> dict:
        """태그별 포스팅 개수를 반환합니다."""
        # 고정 페이지를 제외하고 태그를 수집합니다.
        all_tags_tuples = db.query(self.model.tags).filter(
            self.model.tags.isnot(None),
            self.model.slug.is_(None)  # slug가 없는 일반 게시글만
        ).all()
        
        tag_counts = {}
        for tags_tuple in all_tags_tuples:
            tags_str = tags_tuple[0]
            if tags_str:
                tags_list = [tag.strip() for tag in tags_str.split(',')]
                for tag in tags_list:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return tag_counts

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Board]:
        return db.query(Board).filter(Board.slug == slug).first()

    def get_by_id_or_slug(self, db: Session, *, post_id: Union[int, str]) -> Optional[Board]:
        """
        ID(숫자) 또는 Slug(문자)를 받아 게시글을 조회합니다.
        FastAPI 경로 파라미터는 문자열로 전달되므로, 숫자로 변환 가능한지 확인합니다.
        """
        # --- [핵심 수정] ---
        # post_id가 숫자로만 이루어진 문자열인지 확인합니다.
        if str(post_id).isdigit():
            # 숫자이면, 정수(int)로 변환하여 id로 조회합니다.
            return db.query(self.model).filter(self.model.id == int(post_id)).first()
        else:
            # 숫자가 아니면, slug로 조회합니다.
            return db.query(self.model).filter(self.model.slug == str(post_id)).first()

board = CRUDBoard(Board)