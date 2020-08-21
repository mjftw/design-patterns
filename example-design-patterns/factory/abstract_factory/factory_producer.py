from .factories import AnimalFactory, InstrumentFactory
from .factory import IAbstractFactory, IFactory


class FactoryProducer(IAbstractFactory):
    def get(self, type: str) -> IFactory:
        if type == 'instrument':
            return InstrumentFactory()
        elif type == 'animal':
            return AnimalFactory()
        else:
            raise AttributeError(f'Invalid factory: {type}')
