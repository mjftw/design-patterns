from sound_maker import ISoundMaker

class IInstrument(ISoundMaker):
    pass


class Guitar(IInstrument):
    def make_sound(self):
        print('Guitar: twang!')


class Drum(IInstrument):
    def make_sound(self):
        print('Drum: bang!')

