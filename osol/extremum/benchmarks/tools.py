from contracts import contract
from joblib import Parallel, delayed


@contract
def benchmark_algorithm(algorithm, benchmarks, terminator, number_of_runs, n_jobs=1):
    """ Performs benchmarking process

    :param algorithm: target algorithm
    :type algorithm: Algorithm

    :param benchmarks: benchmarks to be used
    :type benchmarks: dict(str:Benchmark)

    :param terminator: termination criterion generator
    :type terminator: *

    :param number_of_runs: how many times the algorithm should be tested
    :type number_of_runs: int

    :param n_jobs: parameter for parallelization
    :type n_jobs: int

    :returns: algorithm application results
    :rtype: dict(str:tuple(list(Vector), list(number),number))
    """
    results = dict()
    for b_name, b_func in benchmarks.items():
        search_area = b_func.search_area
        bt = terminator(b_func)
        results[b_name] = []

        def run_algorithm(_):
            return algorithm.optimize(bt, search_area)

        x = Parallel(n_jobs=n_jobs)(delayed(run_algorithm)(_) for _ in range(number_of_runs))
        y = [b_func(x_) for x_ in x]
        results[b_name] = (x, y, b_func.solution[1])
    return results


@contract(returns="dict(str:Benchmark)")
def dim_2():
    """ Returns all 2D benchmark functions """
    return {
        "BartelsConn": BartelsConn(),
        "Beale": Beale(),
        "Bird": Bird(),
        "Bohachevsky": Bohachevsky(),
        "Booth": Booth(),
        "BraninRCOS": BraninRCOS(),
        "Brent": Brent(),
        "Bukin": Bukin(),
        "CamelThreeHumps": CamelThreeHumps(),
        "Chichinadze": Chichinadze(),
        "Cube": Cube(),
        "Damavandi": Damavandi(),
        "DeckkersAarts": DeckkersAarts(),
        "Easom": Easom(),
        "EggCrate": EggCrate(),
        "EggHolder": EggHolder(),
        "Goldstein": Goldstein(),
        "Hansen": Hansen(),
        "Himmelblau": Himmelblau(),
        "Hosaki": Hosaki(),
        "JennrichSampson": JennrichSampson(),
        "Keane": Keane(),
        "Langermann": Langermann(),
        "Leon": Leon(),
        "Matyas": Matyas(),
        "McCormick": McCormick(),
        "Parsopoulos": Parsopoulos(),
        "PenHolder": PenHolder(),
        "Periodic": Periodic(),
        "Price": Price(),
        "Quadratic": Quadratic(),
        "RosenbrockModified": RosenbrockModified(),
        "RotatedEllipse": RotatedEllipse(),
        "Rump": Rump(),
        "SchaffersFirst": SchaffersFirst(),
        "SchaffersSecond": SchaffersSecond(),
        "SchaffersThird": SchaffersThird(),
        "Trecanni": Trecanni(),
        "Trefethen": Trefethen(),
        "Ursem": Ursem()
    }
