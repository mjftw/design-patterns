from .ifactory import IFactory
from .animals import Dog, Cat, IAnimal


class AnimalFactory(IFactory):
    def get(self, name: str) -> IAnimal:
        if name == 'dog':
            return Dog()
        elif name == 'cat':
            return Cat()
        else:
            raise AttributeError(f'Invalid species: {name}')
