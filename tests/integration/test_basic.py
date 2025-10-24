from tests.fixtures.app_examples.basic import port
import pytest
from pygeist_client import PygeistClient


@pytest.mark.asyncio
async def test_main(port):
    c = PygeistClient()
    await c.link('localhost', port)
    res = await c.get('/')
    assert res.status == 200
    assert res.body == 'Hello world!'
    await c.unlink()
