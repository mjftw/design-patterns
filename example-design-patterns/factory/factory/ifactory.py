import abc


class IFactory(metaclass=abc.ABCMeta):
    '''Interface for creating object factories'''

    @abc.abstractmethod
    def get(self, name: str):
        '''Get a new instance from the factory'''
