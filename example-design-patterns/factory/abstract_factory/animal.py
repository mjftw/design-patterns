from .sound_maker import ISoundMaker


class Dog(ISoundMaker):
    def make_sound(self):
        print('Dog: Bark!')


class Cat(ISoundMaker):
    def make_sound(self):
        print('Cat: Meow!')
