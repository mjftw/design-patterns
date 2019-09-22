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


class Transport:
    ''' Interface class, used to pass function calls to another
        object. The concerete class will impliment this interface
        with a given transport protocol. E.g. Http requests.
    '''
    def send(self, msg):
        raise NotImplementedError

    def recieve(self, msg):
        raise NotImplementedError


class QueueTransport(Transport):
    def __init__(self, queue):
        self.queue = queue

    def send(self, msg):
        self.queue.put(msg)

    def recieve(self):
        return self.queue.get()


# Client object helper
class ProxyClient:
    ''' The ProxyClient spoofs another object, pretending to be it.
        Any calls made to the ProxyClient are encoded into a message
        by a Codec, and then handed to a Transport class and sent
        to the ProxyService. '''
    def __init__(self, codec, transport):
        assert isinstance(codec, Codec)
        assert isinstance(transport, Transport)
        self.transport = transport
        self.codec = codec

    def __getattribute__(self, name):
        msg_out = self.codec.encode('__getattribute__', (name,))
        msg_in = self.transport.send(msg_out)
        response = self.codec.decode(msg_in)

        return response


# Service object helper
class ProxyService:
    ''' The ProxyService handles calls ftom the ProxyClient via
        the Transport class. It then makes these same calls to
        the real object that the ProxyClient is spoofing.
        The response is then passed back to the ProxyClient via
        the Transport and handed back to the calling object'''
    def __init__(self, service, codec, transport):
        assert isinstance(codec, Codec)
        assert isinstance(transport, Transport)
        self.service = service
        self.transport = transport
        self.codec = codec

    def run(self):
        while True:
            msg_in = self.transport.recieve()
            (fn_name, args, kwargs) = self.codec.decode(msg_in),
            try:
                fn = getattr(self.service, fn_name)
                response = None
            except AttributeError as e:
                response = e

            if not response:
                try:
                    response = fn(*args, **kwargs)
                except Exception as e:
                    response = e

            msg_out = self.codec.encode(response)
            self.transport.send(msg_out)
