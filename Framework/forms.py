import abc
from abc import ABC


class Forms(ABC):
    @abc.abstractmethod
    def create(self):
        pass