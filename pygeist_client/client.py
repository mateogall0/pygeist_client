from pygeist_client import _adapter
from pygeist_client.response import Response
from pygeist_client.exceptions import FailedResponseProcess
from pygeist_client.abstract.methods_handler import AsyncMethodHandler
import asyncio
import threading


class PygeistClient(AsyncMethodHandler):
    def __init__(self,
                 unresolved_payload_capacity = 2,
                 resolved_payload_capacity = 2,
                 ) -> None:
        self.c = _adapter._create_client(unresolved_payload_capacity,
                                         resolved_payload_capacity)
        self._loop = None
        self._loop_ready = threading.Event()
        self._task = None
        self._thread = None

    def connect(self,
                url: str,
                port: int,
                ) -> None:
        _adapter._connect_client(self.c, url, port)
        self._start_process_input()

    async def _process_input(self) -> None:
        try:
            while True:
                await self._loop.run_in_executor(None,
                                                 _adapter._listen_client_input,
                                                 self.c)
                await self._loop.run_in_executor(None,
                                                 _adapter._process_client_input,
                                                 self.c)
        except asyncio.CancelledError:
            pass

    def _start_process_input(self):
        if self._loop is None:
            def loop_thread():
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
                self._loop_ready.set()
                self._loop.run_forever()

            self._thread = threading.Thread(target=loop_thread, daemon=True)
            self._thread.start()
            self._loop_ready.wait()

        if self._task is None:
            self._task = asyncio.run_coroutine_threadsafe(self._process_input(), self._loop)

    def _stop_process_input(self):
        if self._task is not None:
            self._task.cancel()
            self._task = None

    async def _handle(self,
                      method: int,
                      target: str,
                      headers: dict = {},
                      body = '',
                      ) -> Response:
        headers_str = "\r\n".join(f"{k}: {v}" for k, v in headers.items()) + "\r\n"
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
                return await asyncio.to_thread(
                    _adapter._get_client_response,
                    self.c,
                    req_id,
                )
            except FailedResponseProcess:
                pass  # continue until the server replies

    def disconnect(self) -> None:
        _adapter._disconnect_client(self.c)
        self._stop_process_input()

    def __del__(self) -> None:
        self.disconnect()
        _adapter._destroy_client(self.c)
