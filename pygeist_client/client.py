from pygeist_client import _adapter
from pygeist_client.response import Response
from pygeist_client.exceptions import FailedResponseProcess
from pygeist_client.abstract.methods_handler import AsyncMethodHandler
import asyncio
import time
import threading


class PygeistClient(AsyncMethodHandler):
    def __init__(self,
                 unresolved_payload_capacity=2,
                 resolved_payload_capacity=2,
                 ) -> None:
        self.c = _adapter._create_client(unresolved_payload_capacity,
                                         resolved_payload_capacity)
        self._process_thread = None
        self._stop_event = threading.Event()

    def _process_loop(self) -> None:
        try:
            while not self._stop_event.is_set():
                try:
                    _adapter._listen_client_input(self.c)
                    _adapter._process_client_input(self.c)
                except Exception:
                    # sleep briefly to avoid tight loop in failure cases
                    asyncio.run(asyncio.sleep(0))
                    continue
        except Exception:
            pass

    async def link(self,
                   url: str,
                   port: int,
                   ) -> None:
        _adapter._connect_client(self.c, url, port)
        self._stop_event.clear()
        if self._process_thread is None or not self._process_thread.is_alive():
            self._process_thread = threading.Thread(target=self._process_loop, daemon=True)
            self._process_thread.start()

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
                return await asyncio.to_thread(_adapter._get_client_response,
                                               self.c,
                                               req_id)
            except FailedResponseProcess:
                pass # continue until it finds the answer

    async def unlink(self) -> None:
        _adapter._disconnect_client(self.c)
        if self._process_thread and self._process_thread.is_alive():
            self._stop_event.set()
            self._process_thread.join(timeout=1.0)
            self._process_thread = None

    def __del__(self) -> None:
        _adapter._destroy_client(self.c)
