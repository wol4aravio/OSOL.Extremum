from contracts import contract
import numpy as np

from osol.extremum.algorithms.terminator import DummyTerminator, MaxCallsTerminator, MaxTimeTerminator


@contract
def verify(algorithm, number_of_attempts=5, max_iterations=int(5e3), max_calls=int(5e3), max_time="s:1", eps=1e-2):
    """ Verification procedure of optimization algorithms

        :param algorithm: algorithm to be verified
        :type algorithm: Algorithm

        :param number_of_attempts: number of runs if algorithm fails
        :type number_of_attempts: int

        :param max_iterations: number of iterations for `DummyTerminator`
        :type max_iterations: int

        :param max_calls: number of iterations for `MaxCallsTerminator`
        :type max_calls: int

        :param max_time: working time for `MaxTimeTerminator`
        :type max_time: str

        :param eps: maximum acceptable error
        :type eps: float

        :returns: verification result
        :rtype: bool
    """
    limit = 10.0
    search_area = [(-limit, limit) for _ in range(3)]
    optimal_vector = np.random.uniform(-limit, limit, len(search_area))

    success = {
        "d": False,
        "mc": False,
        "mt": False
    }

    def f(v):
        return np.sum(np.square(v - optimal_vector))

    for _ in range(number_of_attempts):
        if not success["d"]:
            d_terminator = DummyTerminator(f, mode="dummy")
            d_result = algorithm.optimize(d_terminator, search_area, max_iterations=max_iterations)
            d_distance = (d_result - optimal_vector).length
            success["d"] = d_distance < eps

        if not success["mc"]:
            mc_terminator = MaxCallsTerminator(f, mode="dummy", max_calls=max_calls)
            mc_result = algorithm.optimize(mc_terminator, search_area)
            mc_distance = (mc_result - optimal_vector).length
            success["mc"] = mc_distance < eps

        if not success["mt"]:
            mt_terminator = MaxTimeTerminator(f, mode="dummy", max_time=max_time)
            mt_result = algorithm.optimize(mt_terminator, search_area)
            mt_distance = (mt_result - optimal_vector).length
            success["mt"] = mt_distance < eps

    return all(success.values())
