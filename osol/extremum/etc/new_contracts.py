from contracts import new_contract
from typing import Callable


new_contract("valid_args_tuple",
             lambda v_: all([isinstance(v, int) or isinstance(v, float) for v in v_]))

new_contract("valid_move_tuples",
             lambda v_: all([isinstance(k, (int, str))
                             and isinstance(d, (int, float)) for k, d in v_]))

new_contract("valid_constrain_tuples",
             lambda v_: all([isinstance(k, (int, str)) and
                             isinstance(min_, (int, float)) and
                             isinstance(max_, (int, float)) for k, (min_, max_) in v_]))

new_contract("Function", Callable)
new_contract("Algorithm", lambda v: type(v).__name__ == "Algorithm" or
                                    type(v).__bases__[0].__name__ == "Algorithm")

new_contract("Terminator", lambda v: type(v).__name__ == "Terminator" or
                                     type(v).__bases__[0].__name__ == "Terminator")

new_contract("Benchmark", lambda v: type(v).__name__ == "OptimizationBenchmark" or
                                    "OptimizationBenchmark" in [t.__name__ for t in type(v).__bases__])
