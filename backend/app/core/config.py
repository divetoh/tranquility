from typing import Any, Optional

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tranquility"
    API_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DEMO_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_OLDDATABASE_URI: Optional[str] = None
    DEMO_USERS: int = 0

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("POSTGRES_SERVER")
        db = values.get("POSTGRES_DB")
        return f"postgresql+asyncpg://{user}:{password}@{host}/{db}"

    BACKEND_CORS_ORIGINS: Optional[str]
    BACKEND_CORS_ORIGINS_LIST: Optional[list[AnyHttpUrl]] = None

    @validator("BACKEND_CORS_ORIGINS_LIST", pre=True)
    def assemble_cors_origins(cls, v: Optional[str], values: dict[str, Any]) -> Optional[list[AnyHttpUrl]]:
        cors = values.get("BACKEND_CORS_ORIGINS")
        if cors is None:
            return None
        cors = cors.strip("'\"")
        if cors == "":
            return None
        return cors.split(",")

    class Config:
        case_sensitive = True


settings = Settings()
