from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Union # ✅ Optional, Union import 추가

from app.crud.base import CRUDBase
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate

class CRUDBoard(CRUDBase[Board, BoardCreate, BoardUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: BoardCreate, owner_id: int) -> Board:
        """
        새로운 게시글을 생성하고, 소유자 ID를 함께 저장합니다.
        """
        # Pydantic 모델을 딕셔너리로 변환
        obj_in_data = obj_in.model_dump()
        # Board 모델 객체 생성
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_tags(self, db: Session, *, tags: List[str], skip: int = 0, limit: int = 100) -> List[Board]:
        """
        제공된 태그 목록 중 하나라도 포함하는 모든 게시글을 조회합니다.
        """
        # 각 태그에 대해 'ilike' 조건을 생성하여 리스트에 담습니다.
        # 'ilike'는 대소문자를 구분하지 않는 검색을 지원합니다.
        filters = [self.model.tags.ilike(f"%{tag}%") for tag in tags]
        # or_ 연산자를 사용하여 여러 조건 중 하나라도 만족하는 경우를 찾습니다.
        return db.query(self.model).filter(or_(*filters)).offset(skip).limit(limit).all()

    def get_all_tags(self, db: Session) -> List[str]:
        """
        데이터베이스에 있는 모든 게시글의 태그를 수집하여 중복을 제거한 전체 태그 목록을 반환합니다.
        """
        # 모든 게시글의 'tags' 컬럼만 조회합니다. 결과는 튜플 리스트로 반환됩니다.
        all_tags_tuples = db.query(self.model.tags).filter(self.model.tags.isnot(None)).all()
        
        # 중복을 허용하지 않는 set을 사용하여 모든 태그를 저장할 변수
        unique_tags = set()

        for tags_tuple in all_tags_tuples:
            # 튜플의 첫 번째 요소가 태그 문자열입니다 (e.g., "tag1, tag2")
            tags_str = tags_tuple[0]
            if tags_str:
                # 쉼표로 태그를 분리하고, 각 태그의 앞뒤 공백을 제거합니다.
                tags_list = [tag.strip() for tag in tags_str.split(',')]
                # set에 여러 태그를 한 번에 추가합니다.
                unique_tags.update(tags_list)
        
        # 최종적으로 set을 리스트로 변환하여 반환합니다.
        return sorted(list(unique_tags))

    # --- [신규 추가] Slug로 게시글을 조회하는 함수 ---
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Board]:
        """
        Slug를 기준으로 게시글을 조회합니다.
        Board 모델에 'slug' 컬럼이 있다고 가정합니다.
        """
        return db.query(self.model).filter(self.model.slug == slug).first()

    # --- [신규 추가] ID 또는 Slug로 게시글을 조회하는 함수 ---
    def get_by_id_or_slug(self, db: Session, *, post_id: Union[int, str]) -> Optional[Board]:
        """
        ID(숫자) 또는 Slug(문자)를 받아 게시글을 조회합니다.
        API 엔드포인트에서 받은 파라미터의 타입에 따라 분기 처리합니다.
        """
        if isinstance(post_id, int):
            # post_id가 숫자이면, 기존처럼 id로 조회
            return db.query(self.model).filter(self.model.id == post_id).first()
        else:
            # post_id가 문자열이면, slug로 조회
            return db.query(self.model).filter(self.model.slug == post_id).first()


board = CRUDBoard(Board)
