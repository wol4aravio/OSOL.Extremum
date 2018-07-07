from abc import ABCMeta, abstractmethod

import os
import shutil
import json


class Algorithm:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def current_state(self):
        '''Returns current state as a dictionary'''

    @property
    @abstractmethod
    def iterations(self):
        '''Returns list of iterations'''

    @abstractmethod
    def initialize(self, f, area, seed):
        '''Initializes algorithm with the given seed'''

    def work(self, f, area, terminator, seed=None, log_states=None):
        self.initialize(f, area, seed)
        if log_states is not None:
            log_counter = 1
            if os.path.exists(log_states):
                shutil.rmtree(log_states)
            os.makedirs(log_states)
        current_iteration = self.iterations[0]

        while not terminator(current_state=self.current_state):
            current_iteration = current_iteration(f, area)
            if current_iteration is None:
                break
            if log_states is not None:
                json.dump(self.current_state, open(os.path.join(log_states, '{0:07d}.json'), 'w'), indent=2)
                log_counter += 1

        return self.current_state['result']

