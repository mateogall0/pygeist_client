import pytest
from pygeist_client.client import PygeistClient
from tests.fixtures.app_examples.basic import port

@pytest.mark.asyncio
async def test_aenter_aexit(port):
    c = PygeistClient()
    assert await c.is_linked() == False
    async with c as client:
        assert await c.is_linked() == False
        await client.link('127.0.0.1', port)
        assert await c.is_linked() == True
        res = await client.get('/')
        assert res.body == 'Hello world!'
        assert await c.is_linked() == True

    assert await c.is_linked() == False
