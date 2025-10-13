from tests.fixtures import math_example_server
from pygeist_client import PygeistClient
import pytest


@pytest.mark.asyncio
async def test_math_server(math_example_server):
    client = PygeistClient()
    client.connect('127.0.0.1', math_example_server)
    res = await client.get('/', {'Operation-Type': 'sum'}, '20')
    assert res
    client.disconnect()
