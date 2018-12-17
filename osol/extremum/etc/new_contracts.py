from contracts import new_contract
from typing import Callable

from osol.extremum.optimization.basic.vector import Vector
from osol.extremum.optimization.basic.algorithm import Algorithm
from osol.extremum.optimization.basic.terminator import Terminator
from osol.extremum.optimization.benchmarks.optimization_benchmark import OptimizationBenchmark


new_contract("Vector",
             lambda v_: isinstance(v_, Vector))

new_contract("valid_args_tuple",
             lambda v_: all([isinstance(v, int) or isinstance(v, float) for v in v_]))

new_contract("valid_move_tuples",
             lambda v_: all([isinstance(k, (int, str))
                             and isinstance(d, (int, float)) for k, d in v_]))

new_contract("valid_constrain_tuples",
             lambda v_: all([isinstance(k, (int, str)) and
                             isinstance(min_, (int, float)) and
                             isinstance(max_, (int, float)) for k, (min_, max_) in v_]))

new_contract("function", Callable)
new_contract("Algorithm", Algorithm)
new_contract("Terminator", Terminator)
new_contract('Benchmark', OptimizationBenchmark)
