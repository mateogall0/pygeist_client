from typing import Any
from pygeist_client._adapter import METHODS
from abc import ABC, abstractmethod


class AsyncMethodHandler(ABC):
    @abstractmethod
    async def _handle(self, method: int, *ag, **kw) -> Any:
        pass


def _make_method(method_value: int):
    async def _method(self, *ag, **kw):
        return await self._handle(method_value, *ag, **kw)
    return _method

for name, value in METHODS.items():
    setattr(AsyncMethodHandler, name.lower(), _make_method(value))
