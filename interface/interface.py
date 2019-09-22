
# Move interface
class Move:
    def move(self):
        raise NotImplementedError


# Impliments Move interface
class WalkMove(Move):
    def move(self):
        print("Walk")


# Impliments Move interface
class FlyMove(Move):
    def move(self):
        print("Flap Flap")


# Sound interface
class Sound:
    def make_sound(self):
        raise NotImplementedError


# Impliments Sound interface
class BarkSound(Sound):
    def make_sound(self):
        print("Bark!")


# Impliments Sound interface
class QuackSound(Sound):
    def make_sound(self):
        print("Quack!")


# Base class has Move and Sound interfaces
class Animal:
    def __init__(self):
        self.Move = Move()
        self.Sound = Sound()

    def make_sound(self):
        self.Sound.make_sound()

    def move(self):
        self.Move.move()


# Extends Animal base class, defining correct Move and Bark interfaces
class Dog(Animal):
    def __init__(self):
        Animal.__init__(self)

        self.Move = WalkMove()
        self.Sound = BarkSound()


# Extends Animal base class, defining correct Move and Bark interfaces
class Duck(Animal):
    def __init__(self):
        Animal.__init__(self)

        self.Move = FlyMove()
        self.Sound = QuackSound()
