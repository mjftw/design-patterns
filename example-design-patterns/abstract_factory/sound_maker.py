import abc


class ISoundMaker(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def make_sound(self):
        pass
