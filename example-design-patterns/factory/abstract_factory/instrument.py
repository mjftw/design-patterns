from .sound_maker import ISoundMaker


class Guitar(ISoundMaker):
    def make_sound(self):
        print('Guitar: twang!')


class Drum(ISoundMaker):
    def make_sound(self):
        print('Drum: bang!')
