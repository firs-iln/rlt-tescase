import asyncio
import logging
from datetime import datetime

from bot.setup import start
from core.SalaryAggregator import SalaryAggregator
from core.enums.AggregationPeriodEnum import AggregationPeriod
from core.schemas import SalaryRecord, Request
from database import Record
from database import init_db
from database.MongoSalaryAsyncQueryable import MongoSalaryAsyncQueryable

logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.StreamHandler(),
                    ],
                    format='%(asctime)s - [%(levelname)s] - %(name)s - '
                           '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
                    )


async def main():
    await init_db()

    salaries = MongoSalaryAsyncQueryable(model=Record, schema=SalaryRecord)

    # aggregator = SalaryAggregator(salaries)
    # print(await aggregator.aggregate(Request(
    #     dt_from=datetime(year=2022, month=2, day=1),
    #     dt_upto=datetime(year=2022, month=2, day=2),
    #     group_type=AggregationPeriod.HOUR
    # )))

    await start(salaries=salaries)


"""
{
   "dt_from": "2022-02-01T00:00:00",
   "dt_upto": "2022-02-02T00:00:00",
   "group_type": "hour"
}
"""
"""
{
   "dt_from": "2022-10-01T00:00:00",
   "dt_upto": "2022-11-30T23:59:00",
   "group_type": "day"
}
"""
if __name__ == '__main__':
    asyncio.run(main())
