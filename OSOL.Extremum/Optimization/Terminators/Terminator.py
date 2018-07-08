from abc import ABCMeta, abstractmethod


class Terminator(dict):
    __metaclass__ = ABCMeta

    @abstractmethod
    def initialize(self):
        '''Initializes terminator'''

    @abstractmethod
    def __call__(self, *args, **kwargs):
        '''Check termination condition'''
