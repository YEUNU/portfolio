from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.page import Page
from app.schemas.page import PageCreate, PageUpdate

class CRUDPage(CRUDBase[Page, PageCreate, PageUpdate]):
    """
    Page 모델에 특화된 데이터베이스 관리(CRUD) 클래스입니다.
    """
    def get_by_slug(self, db: Session, *, slug: str) -> Page | None:
        """
        고유 식별자인 slug를 사용하여 페이지 데이터를 조회합니다.
        
        :param db: 데이터베이스 세션
        :param slug: 조회할 페이지의 slug (e.g., "about", "contact")
        :return: Page 모델 객체 또는 None
        """
        return db.query(self.model).filter(self.model.slug == slug).first()

# CRUDPage 클래스의 인스턴스를 생성하여 다른 파일에서 쉽게 가져다 쓸 수 있도록 함
page = CRUDPage(Page)

