import pickle
import bz2


class Codec:
    ''' Encode function name, args, and kwargs into a
        message. Decode message back into function name, args, and kwargs.
    '''
    def encode(self, fn, *args, **kwargs):
        raise NotImplementedError

    def decode(self, msg):
        raise NotImplementedError


class PickleCodec(Codec):
    def __init__(self, compress=None):
        self.compress = compress or False

    def encode(self, msg_in):
        msg = pickle.dumps(msg_in)
        if self.compress:
            msg = bz2.compress(msg)

        return msg

    def decode(self, msg):
        if self.compress:
            msg = bz2.decompress(msg)

        (fn, args, kwargs) = pickle.loads(msg)
        return (fn, args, kwargs)
