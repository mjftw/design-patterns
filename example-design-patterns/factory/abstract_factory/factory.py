import abc
from abc import abstractmethod


class IFactory(metaclass=abc.ABCMeta):
    '''Interface for creating object factories'''

    @abc.abstractmethod
    def get(self, name: str):
        '''Get a new instance from the factory'''


class IAbstractFactory(metaclass=abc.ABCMeta):
    '''Factory to create factories'''
    @abstractmethod
    def get(self, name: str) -> IFactory:
        '''Get a new factory'''
