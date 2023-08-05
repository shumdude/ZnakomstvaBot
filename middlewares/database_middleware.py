import asyncpg
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database import DBRequest


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, connector: asyncpg.pool.Pool) -> None:
        super().__init__()
        self.connector = connector

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with self.connector.acquire() as connect:
            data["db_request"] = DBRequest()
            return await handler(event, data)
