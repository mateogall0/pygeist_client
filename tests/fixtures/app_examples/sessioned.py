import pytest
from pygeist import (ZeitgeistAPI,
                     Request,
                     send_message,
                     Router,)
from . import find_free_port, server_stop, server_start

@pytest.fixture
def port() -> int:
    _app = ZeitgeistAPI(find_free_port())

    waiting = []

    async def broadcast(msg: str):
        for k in waiting:
            print(f'sending: {msg} to {k}')
            sent = await send_message(k, msg)
            print(f'sent: {sent}')

    async def wait_msg(req: Request):
        waiting.append(req.client_key)

    msgs_r = Router('/msgs')
    msgs_r.post('/', wait_msg, status_code=200)
    msgs_r.post('/broadcast', broadcast, status_code=200)

    _app.include_router(msgs_r)

    p = server_start(_app)

    try:
        yield _app.port
    finally:
        server_stop(p)
