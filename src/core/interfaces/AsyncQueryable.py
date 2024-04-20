from _ast import BoolOp
from abc import abstractmethod
from typing import TypeVar

from pydantic import BaseModel

Schema = TypeVar("Schema", bound=BaseModel, covariant=True)


class AsyncQueryable:
    schema: Schema

    @abstractmethod
    async def get(self, *filters: BoolOp) -> list[Schema]:
        pass
