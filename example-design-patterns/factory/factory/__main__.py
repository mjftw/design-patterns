'''Example of the Factory design pattern'''

from .animal_factory import AnimalFactory


def main():
    factory = AnimalFactory()

    cat = factory.get('cat')
    cat.make_sound()

    dog = factory.get('dog')
    dog.make_sound()


if __name__ == '__main__':
    main()
