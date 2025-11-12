from pygeist_client import _adapter
from pygeist_client.exceptions import FailedConnection
from pygeist_client.response import Response
from pygeist_client.abstract.methods_handler import AsyncMethodHandler
from pygeist_client.unrequested import Unrequested
import asyncio
import json


class PygeistClient(AsyncMethodHandler):
    """
    An asyncronous `Zeitgeist` client with request sender, response receiver,
    and a listener for server unrequested messages

    Can be used in a context-managed way:
    ```python
    >>> async with PygeistClient() as client:
    >>>     await client.link('https://example.org', 8000)
    >>>     response = await client.get('/')
    ```

    or in a manual explicit way:
    ```python
    >>> client = PygeistClient()
    >>> await client.link('https://example.org', 8000)
    >>> response = await client.get('/')
    >>> await client.unlink()
    ```

    """
    def __init__(self,
                 response_timeout=5, # seconds
                 ) -> None:
        self.c = _adapter._create_client(1, 1)
        self.response_timeout = response_timeout

    async def link(self,
                   url: str,
                   port: int,
                   ) -> None:
        """
        Stablish a link to a server that utilizes the Zeitgeist protocol
        This needs to be done before making any request to the server
        """
        if url == 'localhost':
            url = '127.0.0.1'
        await asyncio.to_thread(_adapter._connect_client,
                                self.c,
                                url,
                                port,)

    async def _handle(self,
                      method: int,
                      target: str,
                      headers: dict = {},
                      body: str | dict = '',
                      ) -> Response:
        """
        Build the request payload and listen to receive it and process it
        """
        headers_str = "\r\n".join(f"{k}: {v}" for k, v in headers.items()) + "\r\n\r\n"
        body = body if isinstance(body, str) else json.dumps(body)
        req_id = await asyncio.to_thread(
            _adapter._make_client_request,
            self.c,
            method,
            target,
            headers_str,
            body,
        )

        await asyncio.wait_for(
            asyncio.to_thread(_adapter._listen_client_input,
                              self.c),
            timeout=self.response_timeout,
        )
        await asyncio.to_thread(_adapter._process_client_input,
                                self.c)

        return await asyncio.to_thread(_adapter._get_client_response,
                                       self.c,
                                       req_id)

    async def unlink(self) -> None:
        await asyncio.to_thread(_adapter._disconnect_client,
                                self.c)

    def __del__(self) -> None:
        _adapter._destroy_client(self.c)

    async def pop_msg(self,
                      timeout=5, # seconds
                      ) -> Unrequested | None:
        """
        If there is a message available from the server and is correctly
        formatted, it is going to be popped

        There is a max timeout given to wait for that message to be received
        """
        await asyncio.wait_for(
            asyncio.to_thread(_adapter._listen_client_input,
                              self.c),
            timeout=timeout,
        )
        await asyncio.to_thread(_adapter._process_client_input,
                                self.c)
        return await asyncio.to_thread(_adapter._pop_client_message, self.c)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type != FailedConnection:
            await self.unlink()

    async def is_linked(self) -> bool:
        """
        Returns `True` if the client is already linked
        """
        return _adapter._is_connected(self.c)
