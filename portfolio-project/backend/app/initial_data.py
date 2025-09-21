from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

def init_db(db: Session) -> None:
    """
    데이터베이스에 초기 데이터를 생성합니다.
    (기본 관리자 계정, About/Contact 페이지 등)
    """
    # 1. 기본 관리자 계정 생성
    # settings.FIRST_ADMIN_USERNAME에 해당하는 사용자가 있는지 확인
    user = crud.user.get_by_username(db, username=settings.FIRST_ADMIN_USERNAME)
    if not user:
        # 사용자가 없으면, UserCreate 스키마를 사용하여 새로운 관리자 계정 생성
        user_in = schemas.UserCreate(
            username=settings.FIRST_ADMIN_USERNAME,
            password=settings.FIRST_ADMIN_PASSWORD,
            is_admin=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        print(f"Superuser '{settings.FIRST_ADMIN_USERNAME}' created")
    else:
        print(f"Superuser '{settings.FIRST_ADMIN_USERNAME}' already exists in database")

    # 2. 'About' 페이지 생성
    about_page = crud.page.get_by_slug(db, slug="about")
    if not about_page:
        page_in = schemas.PageCreate(
            slug="about",
            title="About Me",
            content="## 안녕하세요! \n\n이곳에 자신을 소개하는 글을 Markdown 형식으로 작성해보세요."
        )
        crud.page.create(db, obj_in=page_in)
        print("Default 'about' page created")

    # 3. 'Contact' 페이지 생성
    contact_page = crud.page.get_by_slug(db, slug="contact")
    if not contact_page:
        page_in = schemas.PageCreate(
            slug="contact",
            title="Contact",
            content="## 연락처 정보 \n\n- **Email**: your-email@example.com \n- **GitHub**: your-github-id"
        )
        crud.page.create(db, obj_in=page_in)
        print("Default 'contact' page created")

