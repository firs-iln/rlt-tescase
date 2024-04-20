import json
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.SalaryAggregator import SalaryAggregator
from core.interfaces.SalaryAsyncQueryable import SalaryAsyncQueryable
from core.schemas import Request

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('start'))
async def start(message):
    if message.from_user.username:
        await message.answer(f'Hi {message.from_user.username}')
    else:
        await message.answer('Hi!')


@router.message()
async def aggregate(message: Message, salaries: SalaryAsyncQueryable):
    try:
        aggregator = SalaryAggregator(data=salaries)

        request_dict = json.loads(message.text)
        logger.info(f'Got request: {request_dict}')

        request = await Request.from_dict(request_dict)
        response = await aggregator.aggregate(request=request)

        response_str = await response.to_str()
        logger.info(f'Sending response: {response_str}')

        await message.answer(json.dumps(await response.to_dict()))
    except Exception as e:
        logger.error(f'Error: {e}')
        await message.answer('an error occurred, please try again later')
