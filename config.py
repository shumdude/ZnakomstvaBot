from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    database: str = Field(env='POSTGRES_DB')
    db_host: str = Field(env='POSTGRES_HOST')
    db_user: str = Field(env='POSTGRES_USER')
    db_port: str = Field(env='POSTGRES_PORT')
    db_password: str = Field(env='POSTGRES_PASSWORD')

    def db_url(self):
        return f"asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.database}"


class TelegramSettings(BaseSettings):
    token: str = Field(env='BOT_TOKEN')
    admin_ids: list[int] = Field(env='ADMIN_IDS')


class Settings(BaseSettings):
    db = DatabaseSettings()
    tg = TelegramSettings()


settings = Settings()

TORTOISE_ORM = {
    'connections': {'default': settings.db.db_url()},
    'apps': {
        'app': {
            'models': ['database.models', 'aerich.models'],
            'default_connection': 'default'
        },
    },
}
