from interface import Duck, Dog


def main():
    myAnimal = Duck()
    myAnimal.make_sound()
    myAnimal.move()

    myAnimal = Dog()
    myAnimal.make_sound()
    myAnimal.move()


if __name__ == "__main__":
    main()
