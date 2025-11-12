import asyncio
from tests.fixtures.app_examples.sessioned import port
import pytest
from pygeist_client import PygeistClient


@pytest.mark.asyncio
@pytest.mark.parametrize("num_clients,messages", [
    (2, ["hello", "world"]),
    (3, ["foo", "bar", "baz"]),
    (5, ["ping"]),
])
async def test_multiple_clients_broadcast(port, num_clients, messages):
    broadcaster = PygeistClient()
    await broadcaster.link('127.0.0.1', port)

    listeners = [PygeistClient() for _ in range(num_clients)]
    for c in listeners:
        await c.link('127.0.0.1', port)
        res = await c.post('/msgs/')
        assert res.status == 200

    for msg_text in messages:
        res = await broadcaster.post(f'/msgs/broadcast?msg={msg_text}')
        assert res.status == 200

        for c in listeners:
            msg = await asyncio.wait_for(c.pop_msg(), timeout=2)
            assert msg.body == msg_text

    for c in listeners:
        await c.unlink()
    await broadcaster.unlink()


@pytest.mark.asyncio
async def test_no_listeners_broadcast(port):
    c = PygeistClient()
    await c.link('127.0.0.1', port)

    res = await c.post('/msgs/broadcast?msg=lonely')
    assert res.status == 200

    await c.unlink()
