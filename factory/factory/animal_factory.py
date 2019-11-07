from animal import Dog, Cat

class AnimalFactory:
    def get(self, type):
        if type == 'dog':
            return Dog()
        elif type == 'cat':
            return Cat()
        else:
            raise AttributeError(f'Invalid species: {type}')
