"""Tests for termination tools."""


import pytest
from osol.extremum.algorithms.termination import (
    TerminationException,
    TerminationViaMaxCalls,
)


def test_termination_via_max_calls():
    """Test TerminationViaMaxCalls."""

    def f(x):
        return x + 1

    f_term = TerminationViaMaxCalls(f, 5)
    for i in range(5):
        assert f(i) == f_term(i)
    with pytest.raises(TerminationException):
        assert f(i) == f_term(i)
