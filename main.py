import asyncio
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from tortoise import Tortoise
import handlers
from aiogram import Bot, Dispatcher
from config import settings, TORTOISE_ORM
from aerich import Command


async def start():
    # Logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    logger.info('Starting telegram bot')

    # Bot, Storage, Dispatcher
    logger.info("Bot, Storage, Dispatcher...")
    bot: Bot = Bot(token=settings.tg_bot.token, parse_mode='HTML')
    storage: MemoryStorage = MemoryStorage()  # Сменить на Redis
    dp: Dispatcher = Dispatcher(storage=storage)

    # Tortoise-ORM
    logger.info("Tortoise...")
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    # Migrations
    logger.info("Migrations...")
    command = Command(tortoise_config=settings, location="database/migrations/app")
    await command.init()
    await command.init_db(safe=True)
    await command.migrate()
    await command.upgrade(run_in_transaction=True)

    # Вносим роутеры в диспетчер
    logger.info("Register handlers...")
    dp.include_router(handlers.base_router)
    dp.include_router(handlers.registration_router)
    dp.include_router(handlers.search_router)

    # Start polling
    try:
        await bot.delete_webhook(True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


# Start telegram bot
if __name__ == "__main__":
    asyncio.run(start())
