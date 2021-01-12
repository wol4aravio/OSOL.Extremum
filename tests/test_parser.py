"""Set of tests for parser tool."""


import pytest
from numpy.testing import assert_almost_equal

from osol.extremum.tools.parser import OptTask


def test_parser_smoke_1_1():
    """Test #1 parser for smoke_1 function."""
    f = OptTask("osol/extremum/functions/smoke_1.json")
    assert_almost_equal(f(1, 2), 5.0)


def test_parser_smoke_1_2():
    """Test #2 parser for smoke_1 function."""
    f = OptTask("osol/extremum/functions/smoke_1.json")
    assert_almost_equal(f(x=1, y=2), 5.0)


def test_parser_smoke_1_3():
    """Test #3 parser for smoke_1 function."""
    f = OptTask("osol/extremum/functions/smoke_1.json")
    assert_almost_equal(f(y=2, x=1), 5.0)


def test_parser_smoke_1_4():
    """Test #4 parser for smoke_1 function."""
    f = OptTask("osol/extremum/functions/smoke_1.json")
    assert_almost_equal(f(1, y=2), 5.0)


def test_parser_smoke_1_5():
    """Test #5 parser for smoke_1 function."""
    f = OptTask("osol/extremum/functions/smoke_1.json")
    with pytest.raises(ValueError):
        f(1, x=2)
