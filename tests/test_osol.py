"""
Dummy tests.
"""


import importlib_metadata


def test_version():
    """Check version available."""
    assert importlib_metadata.version("osol")
