from pydantic_settings import BaseSettings
from typing import List, Optional, Any
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "My Portfolio API"
    API_V1_STR: str = "/api/v1"

    # 초기 관리자 계정 설정
    FIRST_ADMIN_USERNAME: str
    FIRST_ADMIN_PASSWORD: str

    # JWT 토큰 설정
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 2  # 2시간 (기본값)
    ADMIN_SESSION_TIMEOUT_MINUTES: int = 30  # 관리자 세션 타임아웃 (30분)

    # PostgreSQL Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    DATABASE_URI: Optional[str] = None

    @field_validator("DATABASE_URI", mode='before')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
        
        values = info.data
        return (
            f"postgresql+psycopg2://{values.get('POSTGRES_USER')}:"
            f"{values.get('POSTGRES_PASSWORD')}@"
            f"{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
        )

    # ✅ 수정: CORS 설정을 모든 주소('*')에서 오는 요청을 허용하도록 변경
    # 실제 프로덕션 환경에서는 보안을 위해 특정 도메인 주소만 명시하는 것이 좋습니다.
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

