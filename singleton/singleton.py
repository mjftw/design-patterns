class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance


class MyClass(Singleton):
    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
