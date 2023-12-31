from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import get_profile_by_id
from settings import LEXICON


class RegistrationYetFilter(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        profile = await get_profile_by_id(message.from_user.id)
        if profile:
            await message.reply(LEXICON["registration_yet"])
            await state.clear()
            return False
        else:
            return True
