"""
The config module contains the Settings class which is the place for all backend related settings
like database connection, API keys for third party services, CORS_ORIGINS etc.

Most settings are secret and are therefore read from the environment variables.
"""

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, PostgresDsn, validator


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """
    Here we save all settings which are needed for the backend like database credentials
    The values for each setting is take from environment variables with the same name
    """

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # pylint: disable=no-self-use,no-self-argument
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Makes sure that BACK_CORS_ORIGINS is a list
        """
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    PROJECT_NAME: str

    # DATABASE
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # pylint: disable=no-self-use,no-self-argument
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, value: Optional[str], values: Dict[str, Any]) -> Any:
        """
        Creates a database URI from given database credentials
        """
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # PAPERTRAIL
    PAPERTRAIL_HOST: AnyUrl
    PAPERTRAIL_PORT: int

    # AUTH0
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_BASE_URL: AnyHttpUrl
    AUTH0_JWKS_URL: AnyHttpUrl
    AUTH0_AUDIENCE: AnyHttpUrl
    AUTH0_ISSUER: AnyHttpUrl
    AUTH0_ALGORITHMS: str

    class Config:
        """
        This class makes sure that we read the secrets from the .env file
        """

        env_file = ".env"
        case_sensitive = True


settings = Settings()
