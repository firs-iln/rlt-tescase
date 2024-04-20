from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core import SalaryAsyncQueryable


class DBMiddleware(BaseMiddleware):
    def __init__(self, salaries: SalaryAsyncQueryable):
        self.salaries = salaries

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['salaries'] = self.salaries

        return await handler(event, data)
