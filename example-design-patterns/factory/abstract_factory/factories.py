from .factory import IAbstractFactory
from .instrument import Guitar, Drum
from .animal import Dog, Cat


class InstrumentFactory(IAbstractFactory):
    def get(self, name):
        if name == 'drum':
            return Drum()
        elif name == 'guitar':
            return Guitar()
        else:
            raise AttributeError(f'Invalid instrument: {name}')


class AnimalFactory(IAbstractFactory):
    def get(self, name):
        if name == 'dog':
            return Dog()
        elif name == 'cat':
            return Cat()
        else:
            raise AttributeError(f'Invalid species: {name}')
