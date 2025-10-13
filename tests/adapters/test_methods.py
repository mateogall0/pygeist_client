from pygeist_client import _adapter


def test_has_methods():
    methods = ['POST', 'GET', 'PUT', 'DELETE']

    for m in methods:
        assert(isinstance(getattr(_adapter, m), int))
