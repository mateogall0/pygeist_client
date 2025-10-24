import pytest
from pygeist import ZeitgeistAPI, Request
from . import find_free_port, server_stop, server_start

@pytest.fixture
def port() -> int:
    _app = ZeitgeistAPI(find_free_port())

    async def main(req: Request):
        return 'Hello world!'

    _app.get('/', main, status_code=200)

    p = server_start(_app)

    try:
        yield _app.port
    finally:
        server_stop(p)
