class IAnimal:
    def make_sound(self):
        raise NotImplementedError

class Dog(IAnimal):
    def make_sound(self):
        print('Dog: Bark!')

class Cat(IAnimal):
    def make_sound(self):
        print('Cat: Meow!')