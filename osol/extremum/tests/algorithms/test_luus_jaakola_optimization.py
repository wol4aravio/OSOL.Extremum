from osol.extremum.algorithms.luus_jaakola_optimization import LuusJaakolaOptimization
from osol.extremum.tests.algorithms.verifier import verify


def test():
    ars = LuusJaakolaOptimization(
        init_radius=2.5,
        number_of_samples=5,
        reduction_coefficient=0.95,
        recover_coefficient=0.97,
        iteration_per_run=5)
    assert verify(ars)
