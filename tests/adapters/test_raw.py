from pygeist_client import _adapter
from pygeist_client.exceptions import FailedConnection
import pytest


def test_create_delete_noargs():
    c = _adapter._create_client()
    _adapter._destroy_client(c)

def test_connection_failure():
    c = _adapter._create_client(2, 2)

    with pytest.raises(FailedConnection):
        _adapter._connect_client(c, "127.0.0.1", 8000)

    _adapter._destroy_client(c)
