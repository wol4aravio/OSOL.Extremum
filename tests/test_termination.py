"""Tests for termination tools."""


import pytest

from osol.extremum.algorithms.termination import (
    TerminationException,
    TerminationViaMaxCalls,
)
from osol.extremum.tools.parser import OptTask


def test_termination_via_max_calls():
    """Test TerminationViaMaxCalls."""

    f = OptTask({"function": "x + 1", "vars": ["x"]})

    f.add_termination_criterion(TerminationViaMaxCalls(5))
    for i in range(5):
        assert f(i) == i + 1
    with pytest.raises(TerminationException):
        assert f(i) == 6
