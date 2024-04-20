import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.handlers import router
from bot.middlewares.DBMiddleware import DBMiddleware
from config import bot_config
from core import SalaryAsyncQueryable

logger = logging.getLogger(__name__)


async def start_bot(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send_message(bot_config.ADMIN_ID, text='bot is started')


async def stop_bot(bot: Bot):
    await bot.send_message(bot_config.ADMIN_ID, text='bot is stopped')


async def setup_bot(salaries: SalaryAsyncQueryable):
    bot = Bot(token=bot_config.TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot=bot)

    dp.update.middleware(DBMiddleware(salaries=salaries))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_router(router=router)

    return bot, dp


async def start(salaries: SalaryAsyncQueryable):
    try:
        bot, dispatcher = await setup_bot(salaries=salaries)
        try:
            await dispatcher.start_polling(bot)
        finally:
            await bot.session.close()
    except Exception as e:
        logger.error(f'Error: {e}')
