from abc import ABC, abstractmethod
from contracts import contract, new_contract, with_metaclass, ContractsMeta


class Algorithm(with_metaclass(ContractsMeta, ABC)):
    """ Abstract class that describes desired interface for optimization algorithm """
    __metaclass__ = ContractsMeta