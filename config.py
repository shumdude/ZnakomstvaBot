from environs import Env
from pydantic.dataclasses import dataclass


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_port: str  # Порт базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None):
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                  db=DatabaseConfig(database=env('POSTGRES_DB'),
                                    db_host=env('POSTGRES_HOST'),
                                    db_user=env('POSTGRES_USER'),
                                    db_port=env('POSTGRES_PORT'),
                                    db_password=env('POSTGRES_PASSWORD')))
