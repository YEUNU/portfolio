from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings

def init_db(db: Session) -> None:
    """
    데이터베이스에 초기 데이터를 생성합니다.
    (기본 관리자 계정, About/Contact 페이지 등)
    """
    # 1. 기본 관리자 계정 생성
    user = crud.user.get_by_username(db, username=settings.FIRST_ADMIN_USERNAME)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_ADMIN_USERNAME,
            password=settings.FIRST_ADMIN_PASSWORD,
            is_admin=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        print(f"Superuser '{settings.FIRST_ADMIN_USERNAME}' created")
    else:
        print(f"Superuser '{settings.FIRST_ADMIN_USERNAME}' already exists in database")

    # 2. 'About' 페이지 생성 (Board 테이블 사용)
    # slug를 기준으로 'about' 페이지가 있는지 확인합니다.
    about_page = crud.board.get_by_slug(db, slug="about")
    if not about_page:
        # BoardCreate 스키마를 사용하여 slug를 포함한 페이지 데이터를 생성합니다.
        page_in = schemas.BoardCreate(
            title="About Me",
            content="## 안녕하세요! \n\n이곳에 자신을 소개하는 글을 Markdown 형식으로 작성해보세요.",
            tags="info",
            slug="about"  # <-- 핵심: slug 값을 명시적으로 지정
        )
        crud.board.create_with_owner(db, obj_in=page_in, owner_id=user.id)
        print("Default 'about' page created")

    # 3. 'Contact' 페이지 생성 (Board 테이블 사용)
    contact_page = crud.board.get_by_slug(db, slug="contact")
    if not contact_page:
        page_in = schemas.BoardCreate(
            title="Contact",
            content="## 연락처 정보 \n\n- **Email**: your-email@example.com \n- **GitHub**: your-github-id",
            tags="info",
            slug="contact" # <-- 핵심: slug 값을 명시적으로 지정
        )
        crud.board.create_with_owner(db, obj_in=page_in, owner_id=user.id)
        print("Default 'contact' page created")
