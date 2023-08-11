import os
from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    database: str = Field(default="aaa", env='POSTGRES_DB')
    db_host: str = Field(default="127.0.0.1", env='POSTGRES_HOST')
    db_user: str = Field(default="aa", env='POSTGRES_USER')
    db_port: str = Field(default="5432", env='POSTGRES_PORT')
    db_password: str = Field(default="a", env='POSTGRES_PASSWORD')

    def db_url(self):
        return f"asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.database}"


class TelegramSettings(BaseSettings):
    token: str = Field(default="token", env='BOT_TOKEN')
    admin_ids: list[int] = Field(default=[0], env='ADMIN_IDS')


class Settings(BaseSettings):
    print(f"{os.path.dirname(os.path.abspath(__file__))}\.env")
    db = DatabaseSettings()
    tg = TelegramSettings()

    class Config:
        env_file: str = f"{os.path.dirname(os.path.abspath(__file__))}\.env"


settings = Settings(_env_file=f"{os.path.dirname(os.path.abspath(__file__))}/.env")

TORTOISE_ORM = {
    'connections': {'default': settings.db.db_url()},
    'apps': {
        'app': {
            'models': ['database.models', 'aerich.models'],
            'default_connection': 'default'
        },
    },
}
