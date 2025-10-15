from pygeist_client import _adapter


def test_has_methods():
    methods = ['POST', 'GET', 'PUT', 'DELETE', 'CONNECT', 'HEAD', 'OPTIONS',
               'PATCH']

    for m in methods:
        assert(isinstance(_adapter.METHODS[m], int))
