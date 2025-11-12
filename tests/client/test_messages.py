import asyncio
from tests.fixtures.app_examples.sessioned import port
import pytest
from pygeist_client import PygeistClient


@pytest.mark.asyncio
async def test_broadcast(port):
    c0 = PygeistClient()
    c1 = PygeistClient()
    await c0.link('127.0.0.1', port)
    await c1.link('127.0.0.1', port)

    res = await c0.post('/msgs/')
    assert res.status == 200

    res = await c1.post('/msgs/broadcast?msg=hello')
    assert res.status == 200

    msg = await c0.pop_msg()
    print(msg)
    assert msg

    await c0.unlink()
    await c1.unlink()
