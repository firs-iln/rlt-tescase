from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from core.enums.AggregationPeriodEnum import AggregationPeriod


class Request(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: AggregationPeriod

    @staticmethod
    async def from_dict(data: dict[str, str]) -> Request:
        return Request(
            dt_from=datetime.fromisoformat(data['dt_from']),
            dt_upto=datetime.fromisoformat(data['dt_upto']),
            group_type=AggregationPeriod[data['group_type'].upper()],
        )


class Response(BaseModel):
    dataset: list[int]
    labels: list[datetime]

    async def to_dict(self) -> dict[str, list[str]]:
        return {
            "dataset": [x for x in self.dataset],
            "labels": [x.isoformat() for x in self.labels],
        }

    async def to_str(self) -> str:
        return ('{' + f'"dataset": {self.dataset},\n"labels": {[x.isoformat() for x in self.labels]}' + '}\n').replace("'", '"')


class SalaryRecord(BaseModel):
    dt: datetime
    value: int
