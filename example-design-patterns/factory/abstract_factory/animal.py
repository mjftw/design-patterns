from sound_maker import ISoundMaker


class IAnimal(ISoundMaker):
    def make_sound(self):
        raise NotImplementedError


class Dog(IAnimal):
    def make_sound(self):
        print('Dog: Bark!')


class Cat(IAnimal):
    def make_sound(self):
        print('Cat: Meow!')
