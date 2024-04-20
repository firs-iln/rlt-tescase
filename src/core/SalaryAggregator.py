from datetime import datetime, timedelta

from core.enums.AggregationPeriodEnum import AggregationPeriod
from core.interfaces.SalaryAsyncQueryable import SalaryAsyncQueryable
from core.schemas import Request, Response, SalaryRecord


class SalaryAggregator:
    def __init__(self, data: SalaryAsyncQueryable):
        self.data = data

    async def aggregate(self, request: Request) -> Response:
        upto = await self.get_upto(request)
        request.dt_upto = upto

        target_data: list[SalaryRecord] = await self.data.get(self.data.dt >= request.dt_from,
                                                              self.data.dt <= request.dt_upto)

        labels = await self.get_labels(request)
        res = Response(dataset=[0 for _ in range(len(labels))], labels=labels)

        for record in target_data:
            period_index = await self.get_period_index(request, record)
            if period_index >= len(res.dataset):
                continue

            res.dataset[period_index] += record.value

        return res

    @staticmethod
    async def get_upto(request: Request) -> datetime:
        match request.group_type:
            case AggregationPeriod.HOUR:
                return request.dt_upto
            case AggregationPeriod.DAY:
                return request.dt_upto
            case AggregationPeriod.MONTH:
                return request.dt_upto + timedelta(days=31)
            case _:
                raise ValueError("Invalid aggregation period")

    @staticmethod
    async def get_period_index(request: Request, record: SalaryRecord) -> int:
        match request.group_type:
            case AggregationPeriod.HOUR:
                return int((record.dt - request.dt_from).total_seconds() / 3600)
            case AggregationPeriod.DAY:
                return (record.dt - request.dt_from).days
            case AggregationPeriod.MONTH:
                return (record.dt.year - request.dt_from.year) * 12 + record.dt.month - request.dt_from.month
            case _:
                raise ValueError("Invalid aggregation period")

    @staticmethod
    async def get_labels(request: Request) -> list[datetime]:
        match request.group_type:
            case AggregationPeriod.HOUR:
                periods_count = int((request.dt_upto - request.dt_from).total_seconds() / 3600) + 1
                return [request.dt_from + timedelta(hours=i) for i in range(periods_count)]
            case AggregationPeriod.DAY:
                periods_count = int((request.dt_upto - request.dt_from).total_seconds() / 86400) + 1
                return [request.dt_from + timedelta(days=i) for i in range(periods_count)]
            case AggregationPeriod.MONTH:
                periods_count: int = ((request.dt_upto.year - request.dt_from.year) * 12 +
                                      request.dt_upto.month - request.dt_from.month)
                return [datetime(year=request.dt_from.year + (request.dt_from.month + i) // 13,
                                 month=(request.dt_from.month + i) % 13,
                                 day=1
                                 ) for i in range(periods_count)]
            case _:
                raise ValueError("Invalid aggregation period")
