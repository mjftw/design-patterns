from abstract_factory import AbstractFactory
from instrument import Guitar, Drum

class InstrumentFactory(AbstractFactory):
    def get(self, type):
        if type == 'drum':
            return Drum()
        elif type == 'guitar':
            return Guitar()
        else:
            raise AttributeError(f'Invalid instrument: {type}')