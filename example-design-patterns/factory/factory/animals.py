import abc


class IAnimal(metaclass=abc.ABCMeta):
    '''Animals can move and make a sound'''
    @abc.abstractmethod
    def make_sound(self):
        pass


class Dog(IAnimal):
    def make_sound(self):
        print('Dog: Bark!')


class Cat(IAnimal):
    def make_sound(self):
        print('Cat: Meow!')
