from tests.fixtures.app_examples.basic import port
import pytest
from pygeist_client import PygeistClient
from pygeist_client.exceptions import NotConnected


@pytest.mark.asyncio
async def test_main(port):
    c = PygeistClient()
    await c.link('localhost', port)
    res = await c.get('/')
    assert res.status == 200
    assert res.body == 'Hello world!'
    await c.unlink()

@pytest.mark.asyncio
async def test_not_linked(port):
    c = PygeistClient()
    with pytest.raises(NotConnected):
        await c.get('/')

@pytest.mark.asyncio
async def test_unlinked(port):
    c = PygeistClient()
    await c.link('localhost', port)
    res = await c.get('/')
    assert res.status == 200
    assert res.body == 'Hello world!'
    await c.unlink()
    with pytest.raises(NotConnected):
        await c.get('/')
