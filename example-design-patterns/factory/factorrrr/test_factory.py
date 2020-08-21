import pytest

from .animals import Cat, Dog, IAnimal
from .animal_factory import AnimalFactory


@pytest.fixture
def animalfactory():
    return AnimalFactory()


def test_AnimalFactory_should_get_IAnimals(animalfactory):
    animal = animalfactory.get('cat')
    assert isinstance(animal, IAnimal)


def test_AnimalFactory_should_get_cats(animalfactory):
    animal = animalfactory.get('cat')
    assert isinstance(animal, Cat)


def test_AnimalFactory_should_get_dogs(animalfactory):
    animal = animalfactory.get('dog')
    assert isinstance(animal, Dog)


def test_AnimalFactory_should_error_on_unknown_animal(animalfactory):
    with pytest.raises(AttributeError):
        animalfactory.get('plumbus')
