from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from settings import LEXICON


class AgeFilter(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message, state: FSMContext) -> bool | dict[str, int]:
        numbers = [int(x) for x in message.text.split() if x.isdigit()]
        if numbers:
            age: int = numbers[0]
            if age >= 16:
                return {"age": age}
            else:
                await message.reply(LEXICON["not_16"])
                await state.clear()
                return False
        else:
            await message.reply("Введите ваш возраст:")
            return False
