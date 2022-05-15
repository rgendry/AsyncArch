import pydantic
from sqlalchemy.engine.url import URL


class Settings(pydantic.BaseSettings):
    SERVICE_NAME: str = "TaskTracker"
    ROOT_PATH: str = ""
    DEBUG: bool = False

    DB_DRIVER: str = "postgresql+asyncpg"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "app_pswd"
    DB_DATABASE: str = "app_db"
    DB_ECHO = True

    @property
    def DB_DSN(self) -> URL:  # pylint: disable=invalid-name
        """
        uri подключения к БД
        """
        return URL.create(self.DB_DRIVER, self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_DATABASE)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
