import pytest

from osol.extremum.algorithms.random_search import RandomSearch
from osol.extremum.tools.testing import smoke_check


@pytest.mark.parametrize("_", range(10))
def test_random_search(_):
    assert smoke_check(RandomSearch(1e-1))
