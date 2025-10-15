from pygeist_client import PygeistClient
from pygeist_client.exceptions import FailedConnection
from tests.fixtures import raw_example_server
import pytest


def test_successful(raw_example_server):
    client = PygeistClient()

    client.link('127.0.0.1', raw_example_server)
    client.unlink()


def test_error():
    client = PygeistClient()

    with pytest.raises(FailedConnection):
        client.link('127.0.0.1', 5000)

def test_unconn_disconn():
    client = PygeistClient()

    client.unlink()
