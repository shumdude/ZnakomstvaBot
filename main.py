import asyncio
import logging
import asyncpg
from aiogram.fsm.storage.memory import MemoryStorage
from tortoise import Tortoise
import handlers
from aiogram import Bot, Dispatcher
from config import Config, load_config
# from middlewares import DatabaseMiddleware


# Function to create pool with database
# async def create_pool(config: Config) -> asyncpg.pool.Pool:
#     return await asyncpg.create_pool(user=config.db.db_user,
#                                      password=config.db.db_password,
#                                      host=config.db.db_host,
#                                      database=config.db.database)


async def start():
    # Logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    logger.info('Starting telegram bot')

    # Config, Bot, Dispatcher
    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage: MemoryStorage = MemoryStorage()  # Сменить на Redis
    dp: Dispatcher = Dispatcher(storage=storage)

    # DatabaseMiddleware
    # pool_connect = await create_pool(config)
    # dp.update.middleware.register(DatabaseMiddleware(pool_connect))

    # Tortoise-ORM
    await Tortoise.init(config={
        'connections': {'default': f"asyncpg://"
                                   f"{config.db.db_user}:"
                                   f"{config.db.db_password}@"
                                   f"{config.db.db_host}:"
                                   f"{config.db.db_port}/"
                                   f"{config.db.database}"},
        'apps': {
            'app': {
                'models': ['database.models', 'aerich.models'],
                'default_connection': 'default'
            },
        },
    })
    await Tortoise.generate_schemas()
    logger.info("Tortoise inited!")

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
