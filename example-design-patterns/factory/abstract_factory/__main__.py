'''Example of the Abstract Factory design pattern'''

from .factory_producer import FactoryProducer


def main():
    producer = FactoryProducer()

    animal_factory = producer.get('animal')
    dog = animal_factory.get('dog')
    dog.make_sound()
    cat = animal_factory.get('cat')
    cat.make_sound()

    instrument_factory = producer.get('instrument')
    guitar = instrument_factory.get('guitar')
    guitar.make_sound()
    drum = instrument_factory.get('drum')
    drum.make_sound()


if __name__ == '__main__':
    main()
