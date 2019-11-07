from abstract_factory import AbstractFactory
from instrument_factory import InstrumentFactory
from animal_factory import AnimalFactory


class FactoryProducer:
    def get_factory(self, type):
        if type == 'instrument':
            return InstrumentFactory()
        elif type == 'animal':
            return AnimalFactory()
        else:
            raise AttributeError(f'Invalid factory: {type}')