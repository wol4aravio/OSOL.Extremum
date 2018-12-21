import pytest

from osol.extremum.algorithms.tools import *


@pytest.fixture(scope="session")
def number_of_vectors():
    return int(2.5e3)


@pytest.fixture(scope="session")
def error():
    return 2.5e-2


@pytest.fixture(scope="session")
def number_of_bins():
    return 10


@pytest.fixture(scope="session")
def area():
    return {
        "x": (-1.0, 1.0),
        "y": (-2.0, 2.0),
        "z": (-3.0, 3.0)
    }


@pytest.fixture(scope="session")
def zero():
    return Vector.create(x=0, y=0, z=0)


@pytest.fixture(scope="session")
def radius():
    return 2.0


def test_generate_vector_in_box(number_of_vectors, area, number_of_bins, error):
    vectors = []
    for _ in range(number_of_vectors):
        vectors.append(generate_vector_in_box(area))
        v = vectors[-1]
        assert v == v.constrain(area=area)
    bins = {k: np.linspace(min_, max_, number_of_bins + 1) for k, (min_, max_) in area.items()}
    bins_stat = {k: [0] * number_of_bins for k in area.keys()}
    for vector in vectors:
        for k, v in vector.to_tuples():
            for bin_id, min_ in enumerate(bins[k][:-1]):
                max_ = bins[k][bin_id + 1]
                if min_ <= v <= max_:
                    bins_stat[k][bin_id] += 1 / number_of_vectors
    bins_stat = {k: np.round(occurrences, decimals=3) for k, occurrences in bins_stat.items()}
    for ratios in bins_stat.values():
        assert np.all((ratios - 1.0 / number_of_bins) < error)


def test_generate_vector_in_sphere(number_of_vectors, zero, area, radius):
    for _ in range(number_of_vectors):
        v = generate_vector_in_sphere(zero, radius, area)
        assert v.length <= radius
        assert v == v.constrain(area=area)
