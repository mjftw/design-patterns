import abc
from abc import abstractmethod


class IMovable(metaclass=abc.ABCMeta):
    '''Interface class indicating object can move'''

    @abc.abstractmethod
    def move(self):
        pass


class WalkMove(IMovable):
    '''Fulfills IMovable contract'''

    def move(self):
        print("Walk")


class FlyMove(IMovable):
    '''Fulfills IMovable contract'''

    def move(self):
        print("Flap Flap")


class ISoundable(metaclass=abc.ABCMeta):
    '''Interface indicating that object can make a sound'''
    @abc.abstractmethod
    def make_sound(self):
        pass


class IAnimal(IMovable, ISoundable):
    '''Animals can move and make a sound'''
    pass


class Dog(IAnimal):
    '''Concrete Dog class'''

    def make_sound(self):
        print('Bark!')

    def move(self):
        print('Walk')


class Duck(IAnimal):
    '''Concrete Duck class'''

    def make_sound(self):
        print('Quack!')

    def move(self):
        print('Waddle!')
