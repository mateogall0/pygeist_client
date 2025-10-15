from pygeist_client import _adapter
from pygeist_client.response import Response
from pygeist_client.exceptions import FailedResponseProcess
from pygeist_client.abstract.methods_handler import AsyncMethodHandler
import asyncio
import time
import threading


class PygeistClient(AsyncMethodHandler):
    def __init__(self,
                 response_timeout=5, # seconds
                 ) -> None:
        self.c = _adapter._create_client(1, 1)
        self.response_timeout = response_timeout

    def _process_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                _adapter._listen_client_input(self.c)
                _adapter._process_client_input(self.c)
            except Exception:
                pass

    async def link(self,
                   url: str,
                   port: int,
                   ) -> None:
        _adapter._connect_client(self.c, url, port)

    async def _handle(self,
                      method: int,
                      target: str,
                      headers: dict = {},
                      body = '',
                      ) -> Response:
        headers_str = "\r\n".join(f"{k}: {v}" for k, v in headers.items()) + "\r\n\r\n"
        req_id = await asyncio.to_thread(
            _adapter._make_client_request,
            self.c,
            method,
            target,
            headers_str,
            body,
        )
        while True:
            try:
                await asyncio.wait_for(
                    asyncio.to_thread(_adapter._listen_client_input,
                                      self.c),
                    timeout=self.response_timeout,
                )
                await asyncio.to_thread(_adapter._process_client_input, self.c)

                return await asyncio.to_thread(_adapter._get_client_response,
                                               self.c,
                                               req_id)
            except FailedResponseProcess:
                pass # continue until it finds the answer

    async def unlink(self) -> None:
        _adapter._disconnect_client(self.c)

    def __del__(self) -> None:
        _adapter._destroy_client(self.c)
