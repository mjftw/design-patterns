'''Example usage of Singleton design pattern'''

from .singleton import Singleton


class MyClass(Singleton):
    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2


def main():
    instance1 = MyClass(1, 2)

    print(f'instance1: arg1={instance1.arg1}, arg2={instance1.arg2}')

    instance2 = MyClass(3, 4)

    print(f'instance1: arg1={instance1.arg1}, arg2={instance1.arg2}')
    print(f'instance2: arg1={instance2.arg1}, arg2={instance2.arg2}')

    if instance1 is instance2:
        print('instance1 and instance2 are the same object')
    else:
        print('instance1 and instance2 are not the same object')


if __name__ == '__main__':
    main()
