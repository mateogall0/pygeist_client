# Pygeist Client

[![Tests](https://github.com/mateogall0/pygeist_client/actions/workflows/tests.yml/badge.svg)](https://github.com/mateogall0/pygeist_client/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pygeist Client is a Python module that abstracts the application layer protocol Zeitgeist implementation on the client side.

#### Protocol
See [here](https://github.com/mateogall0/zeitgeist_core) to look into the core implementation of the protocol.

```bash
.
├── core -> zeitgeist_core
├── adapters
├── pygeist_client
└── tests
```

## Installation
This package is available for `pip`:
```bash
pip install pygeist_client
```

## Usage example

Can be used in a context-managed way:
```python
from pygeist_client import PygeistClient
async with PygeistClient() as client:
    await client.link('https://example.org', 8000)
    response = await client.get('/')
```

or in a manual explicit way:
```python
from pygeist_client import PygeistClient
client = PygeistClient()
await client.link('https://example.org', 8000)
response = await client.get('/')
await client.unlink()
```

**Server messages**:
```python
from pygeist_client import PygeistClient
async with PygeistClient() as client:
    await client.link('https://example.org', 8000)
    message = await client.pop_msg(timeout=3)
```

## Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/mateogall0/pygeist_client/issues) or open a [pull request](https://github.com/mateogall0/pygeist_client/pulls).

To set up the project locally:

```bash
git clone https://github.com/mateogall0/pygeist_client
cd pygeist
xargs sudo apt-get -y install < packages.txt
pip install --upgrade pip build twine
pip install .[dev]
make
pytest
```
