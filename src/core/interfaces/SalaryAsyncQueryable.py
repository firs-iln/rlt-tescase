from _ast import BoolOp
from abc import abstractmethod
from typing import Type

from core.interfaces.AsyncQueryable import AsyncQueryable, Schema
from core.schemas import SalaryRecord


class SalaryAsyncQueryable(AsyncQueryable):
    schema: Type[SalaryRecord]

    @abstractmethod
    async def get(self, *filters: BoolOp) -> list[Schema]:
        pass

    @property
    @abstractmethod
    def dt(self):
        pass

    @property
    @abstractmethod
    def value(self):
        pass

    def __init_subclass__(cls, **kwargs):
        cls.schema = SalaryRecord
        super().__init_subclass__(**kwargs)
