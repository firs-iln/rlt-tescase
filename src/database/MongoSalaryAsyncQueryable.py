from __future__ import annotations

from _ast import BoolOp
from typing import Type

from beanie import Document, SortDirection

from core.interfaces.AsyncQueryable import Schema
from core.interfaces.SalaryAsyncQueryable import SalaryAsyncQueryable


class MongoSalaryAsyncQueryable(SalaryAsyncQueryable):
    def __init__(self, model: Type[Document], schema: Type[Schema]):
        self.model = model
        self.schema = schema

    async def get(self, *filters: BoolOp) -> list[Schema]:
        return [self.schema.model_validate(x) for x in await self.model.find(*filters).sort(('dt', SortDirection.ASCENDING)).to_list()]

    @property
    def value(self):
        return self.model.value

    @property
    def dt(self):
        return self.model.dt
