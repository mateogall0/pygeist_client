from typing import Any
from pygeist_client._adapter import (
    POST,
    GET,
    PUT,
    DELETE,
)
from abc import ABC, abstractmethod


class AsyncMethodHandler(ABC):
    @abstractmethod
    async def _handle(self, method: int, *ag, **kw) -> Any:
        pass

    async def post(self, *ag, **kw):
        return await self._handle(POST, *ag, **kw)

    async def get(self, *ag, **kw):
        return await self._handle(GET, *ag, **kw)

    async def put(self, *ag, **kw):
        return await self._handle(PUT, *ag, **kw)

    async def delete(self, *ag, **kw):
        return await self._handle(DELETE, *ag, **kw)
