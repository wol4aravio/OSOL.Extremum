from abc import ABC, abstractmethod
from contracts import contract, new_contract, ContractsMeta


class Algorithm(ABC, metaclass=ContractsMeta):
    """ Abstract class that describes desired interface for optimization algorithm """
    __metaclass__ = ContractsMeta