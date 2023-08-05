from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from settings import LEXICON

base_router: Router = Router()  # Инициализируем роутер уровня модуля


@base_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['start'])
