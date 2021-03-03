"""Tests for algorithm tools."""


import numpy as np
import numpy.testing as npt

from osol.extremum.tools.vectors import bound_vector


def test_bound_vector_1():
    """Test for bound_vector function #1"""
    v = np.array([1, 2, 3])
    bounds = np.array([[-5, 5] * len(v)])
    npt.assert_equal(v, bound_vector(v, bounds))


def test_bound_vector_2():
    """Test for bound_vector function #2"""
    v = np.array([1, 2, 3])
    bounds = np.array([[-2, 2] * len(v)])
    npt.assert_equal(np.array([1, 2, 2]), bound_vector(v, bounds))


def test_bound_vector_3():
    """Test for bound_vector function #3"""
    v = np.array([5, -5, 0])
    bounds = np.array([[-2, 2] * len(v)])
    npt.assert_equal(np.array([2, -2, 0]), bound_vector(v, bounds))
