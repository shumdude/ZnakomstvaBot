from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram import F
from database import *
from database.models import Profile
from keyboards import search_kb

search_router: Router = Router()  # Инициализируем роутер уровня модуля


@search_router.callback_query(F.data == "start_search")
async def start_search_process(callback: CallbackQuery):
    offset: int = await get_offset_by_id(callback.from_user.id)
    profile: Profile = await get_profile_by_offset(offset)
    text: str = f"Имя: {profile.name}\n\n" \
                f"Профиль в телеграм: @{profile.telegram_id}\n\n" \
                f"Возраст: {profile.age}\n\n" \
                f"Информация: {profile.info}\n\n"
    await callback.message.answer(text=text, reply_markup=search_kb)
    await callback.message.edit_reply_markup(None)
    await callback.answer()


@search_router.callback_query(F.data == "next")
async def next_search_process(callback: CallbackQuery):
    offset: int = await get_offset_by_id(callback.from_user.id)
    profile: Profile = await get_profile_by_offset(offset + 1)
    if profile:
        await edit_profile_by_id(user_id=callback.from_user.id,
                                            data={"offset": offset + 1})
        text: str = f"Имя: {profile.name}\n\n" \
                    f"Профиль в телеграм: @{profile.telegram_id}\n\n" \
                    f"Возраст: {profile.age}\n\n" \
                    f"Информация: {profile.info}\n\n"
        await callback.message.edit_reply_markup(None)
        await callback.message.answer(text=text, reply_markup=search_kb)
        await callback.answer()
    else:
        await callback.message.answer(text="Пока что это всё, попробуйте ещё раз позже.")
        await callback.answer()


@search_router.callback_query(F.data == "my_info")
async def my_info_process(callback: CallbackQuery):
    profile: Profile = await get_profile_by_id(callback.from_user.id)
    text: str = f"Имя: {profile.name}\n\n" \
                f"Профиль в телеграм: @{profile.telegram_id}\n\n" \
                f"Возраст: {profile.age}\n\n" \
                f"Информация: {profile.info}\n\n"
    await callback.message.answer(text=text)
    await callback.answer()