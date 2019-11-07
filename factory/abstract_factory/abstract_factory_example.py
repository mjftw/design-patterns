from factory_producer import FactoryProducer


def main():
    producer = FactoryProducer()

    animal_factory = producer.get_factory('animal')
    dog = animal_factory.get('dog')
    dog.make_sound()
    cat = animal_factory.get('cat')
    cat.make_sound()

    instrument_factory = producer.get_factory('instrument')
    guitar = instrument_factory.get('guitar')
    guitar.make_sound()
    drum = instrument_factory.get('drum')
    drum.make_sound()




if __name__ == '__main__':
    main()