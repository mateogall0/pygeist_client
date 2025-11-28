from setuptools import setup, Extension


setup(
    ext_modules=[
        Extension(
            "pygeist_client._adapter",
            sources=["adapters/src/client/placeholder.c"],
            extra_objects=["pygeist_client/_adapter.so"],
        )
    ]
)
