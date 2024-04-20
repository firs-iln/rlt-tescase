import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import db_config
from core import SalaryRecord
from database.restore import restore
from .models import Record

from .MongoSalaryAsyncQueryable import MongoSalaryAsyncQueryable


logger = logging.getLogger(__name__)


async def init_db():
    connection_string = f"mongodb://{db_config.MONGO_INITDB_ROOT_USERNAME}:{db_config.MONGO_INITDB_ROOT_PASSWORD.get_secret_value()}@{db_config.DB_HOST}:{db_config.DB_PORT}"
    client = AsyncIOMotorClient(connection_string)
    await init_beanie(
        database=getattr(client, db_config.DB_NAME),
        document_models=[
            Record,
        ]
    )
    logger.info("DB initialized")

    # await restore("../dump/sampleDB", client, db_config.DB_NAME)


async def get_salaries():
    return MongoSalaryAsyncQueryable(model=Record, schema=SalaryRecord)

__all__ = [
    "init_db",
    "MongoSalaryAsyncQueryable",
]
