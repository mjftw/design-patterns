from transport import Transport
from codec import Codec


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
