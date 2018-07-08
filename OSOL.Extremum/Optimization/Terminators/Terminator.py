from abc import ABCMeta, abstractmethod


class Terminator:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_data):
        '''Constructs terminator from dict'''

    @classmethod
    @abstractmethod
    def from_json(cls, json_data):
        '''Constructs terminator from json'''

    @abstractmethod
    def initialize(self):
        '''Initializes terminator'''

    @abstractmethod
    def __call__(self, *args, **kwargs):
        '''Check termination condition'''
