from aiogram.filters import Command, StateFilter
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from database import add_profile
from filters import AgeFilter, RegistrationYetFilter
from keyboards import start_search_kb
from settings import LEXICON
from states import FSMRegistration

registration_router: Router = Router()  # Инициализируем роутер уровня модуля


# Отмена
@registration_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Ок. Не регистрируем.')
    await state.clear()


# Точка входа - registration
@registration_router.message(Command(commands='registration'), StateFilter(default_state), RegistrationYetFilter())
async def process_fsm_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["registration"])
    await state.set_state(FSMRegistration.age)


# Возраст
@registration_router.message(StateFilter(FSMRegistration.age), AgeFilter())
async def process_name(message: Message, state: FSMContext, age: int):
    await state.update_data(age=age)
    await message.answer(text='Отлично. Теперь назови своё имя:')
    await state.set_state(FSMRegistration.name)


# Имя
@registration_router.message(StateFilter(FSMRegistration.name))
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Последний шаг. Расскажи о себе:')
    await state.set_state(FSMRegistration.info)


# Точка выхода - Информация
@registration_router.message(StateFilter(FSMRegistration.info))
async def process_date_of_birth(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    data = await state.get_data()
    await add_profile(user_id=message.from_user.id,
                      name=data["name"],
                      age=data["age"],
                      info=data["info"],
                      telegram_id=message.from_user.username)
    await state.clear()
    await message.answer(text=LEXICON["registration_ok"], reply_markup=start_search_kb)
