from contracts import contract

from osol.extremum.optimization.benchmarks.optimization_benchmark import *  # Required for `Benchmark` contract inclusion
from osol.extremum.optimization.benchmarks.unconstrained_optimization import *


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
