from tests.fixtures import math_example_server
from pygeist_client import PygeistClient
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "operation, input_value, expected_status, expected_body",
    [
        ("sum", 20, 200, 40.0),
        ("mul", 5, 200, 25.0),
        ("sub", 10, 200, 0.0),
        ("sub", 11110, 200, 0.0),
        ("div", 10, 200, 1.0),
        ("div", 0, 400, None),
        ("invalid", 42, 400, None),
    ]
)
async def test_math_server_all_cases(math_example_server, operation, input_value, expected_status, expected_body):
    client = PygeistClient()
    await client.link('127.0.0.1', math_example_server)

    res = await client.get('/', {'Operation-Type': operation}, str(input_value))

    assert res.status == expected_status
    assert res.body == expected_body

    await client.unlink()
