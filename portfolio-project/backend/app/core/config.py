from pydantic_settings import BaseSettings
from typing import List, Optional, Any
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "My Portfolio API"
    API_V1_STR: str = "/api/v1"

    # --- ✅ 추가된 부분: 초기 관리자 계정 설정 ---
    FIRST_ADMIN_USERNAME: str
    FIRST_ADMIN_PASSWORD: str

    # JWT 토큰 설정
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8일

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

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:8080", "http://localhost"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

