from pygeist_client import PygeistClient
from pygeist_client.exceptions import FailedConnection
from tests.fixtures import raw_example_server
import pytest


@pytest.mark.asyncio
async def test_successful(raw_example_server):
    client = PygeistClient()

    await client.link('127.0.0.1', raw_example_server)
    await client.unlink()

@pytest.mark.asyncio
async def test_error():
    client = PygeistClient()

    with pytest.raises(FailedConnection):
        await client.link('127.0.0.1', 5000)

@pytest.mark.asyncio
async def test_unconn_disconn():
    client = PygeistClient()

    await client.unlink()
