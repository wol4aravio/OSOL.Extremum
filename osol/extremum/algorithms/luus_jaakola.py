from osol.extremum.algorithm import OptimizationAlgorithm
from osol.extremum.tools.vectors import (
    bound_vector,
    generate_vector_in_area,
    generate_vector_in_sphere,
)


class LuusJaakola(OptimizationAlgorithm):
    def __init__(
        self,
        init_radius,
        number_of_samples,
        reduction_coefficient,
        recover_coefficient,
        iteration_per_run,
    ):
        self.init_radius = self._r = init_radius
        self.number_of_samples = number_of_samples
        self.reduction_coefficient = reduction_coefficient
        self.recover_coefficient = recover_coefficient
        self.iteration_per_run = iteration_per_run

        self._run_id = 0
        self._iter_id = 0

    def initialize(self, f, search_area):
        self.x = generate_vector_in_area(search_area)
        self.f_x = f(self.x)

    def iterate(self, f, search_area):
        for _ in range(self.number_of_samples):
            x_new = generate_vector_in_sphere(self.x, self._r)
            x_new = bound_vector(x_new, search_area)
            f_x_new = f(x_new)
            if f_x_new < self.f_x:
                self.x = x_new
                self.f_x = f_x_new

        self._r *= self.reduction_coefficient
        self._iter_id += 1

        if self._iter_id == self.iteration_per_run:
            self._iter_id = 0
            self._run_id += 1
            self._r = (self.recover_coefficient ** self._run_id) * self.init_radius

    def terminate(self, _, __):
        return self.x
