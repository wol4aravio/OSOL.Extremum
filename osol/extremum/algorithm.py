from abc import ABC, abstractmethod
from typing import Callable, List, Tuple

import numpy as np

from intervallum.interval import IntervalNumber
from intervallum.box import BoxVector


class Algorithm(ABC):

    @abstractmethod
    def optimize(
            self,
            f: Callable[[BoxVector], IntervalNumber],
            search_area: List[Tuple[float, float]]) -> np.ndarray:
        ...


