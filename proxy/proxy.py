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
        object.__setattr__(self, '_transport', transport)
        object.__setattr__(self, '_codec', codec)

    def proxy_call(self, fn_name, *args, **kwargs):
        codec = object.__getattribute__(self, '_codec')
        transport = object.__getattribute__(self, '_transport')

        msg_out = codec.encode((fn_name, args, kwargs))
        transport.send(msg_out)
        msg_in = transport.recieve()
        response = codec.decode(msg_in)

        if not callable(response):
            return response

        fn_name = args[0]

        def wrap(*fn_args, **fn_kwargs):
            msg_out = codec.encode((fn_name, fn_args, fn_kwargs))
            transport.send(msg_out)
            msg_in = transport.recieve()
            response = codec.decode(msg_in)

            return response
        wrap.__name__ = fn_name

        return wrap

    #
    # proxying (special cases)
    #
    def __getattr__(self, *args, **kwargs):
        proxy_call = object.__getattribute__(self, 'proxy_call')
        return proxy_call('__getattr__', *args, **kwargs)

    def __delattr__(self, *args, **kwargs):
        proxy_call = object.__getattribute__(self, 'proxy_call')
        return proxy_call('__delattr__', *args, **kwargs)

    def __setattr__(self, *args, **kwargs):
        proxy_call = object.__getattribute__(self, 'proxy_call')
        return proxy_call('__setattr__', *args, **kwargs)

    def __nonzero__(self, *args, **kwargs):
        proxy_call = object.__getattribute__(self, 'proxy_call')
        return proxy_call('__nonzero__', *args, **kwargs)

    def __str__(self, *args, **kwargs):
        proxy_call = object.__getattribute__(self, 'proxy_call')
        return proxy_call('__str__', *args, **kwargs)

    def __repr__(self, *args, **kwargs):
        proxy_call = object.__getattribute__(self, 'proxy_call')
        return proxy_call('__repr__', *args, **kwargs)

    def __hash__(self, *args, **kwargs):
        proxy_call = object.__getattribute__(self, 'proxy_call')
        return proxy_call('__hash__', *args, **kwargs)


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
            decoded = self.codec.decode(msg_in),
            decoded = decoded[0]

            args = ()
            kwargs = {}
            fn_name = None
            response = None

            if len(decoded) >= 1:
                fn_name = decoded[0]
            if len(decoded) >= 2:
                args = decoded[1]
            if len(decoded) >= 3:
                kwargs = decoded[2]

            try:
                if fn_name == '__getattr__':
                    response = object.__getattribute__(self.service, *args, **kwargs)
                elif fn_name == '__delattr__':
                    response = delattr(self.service, *args, **kwargs)
                elif fn_name == '__setattr__':
                    response = setattr(self.service, *args, **kwargs)
                elif fn_name == '__nonzero__':
                    response = bool(self.service, *args, **kwargs)
                elif fn_name == '__str__':
                    response = str(self.service, *args, **kwargs)
                elif fn_name == '__repr__':
                    response = repr(self.service, *args, **kwargs)
                elif fn_name == '__hash__':
                    response = hash(self.service, *args, **kwargs)
                else:
                    fn = object.__getattribute__(self.service, fn_name)
                    response = fn(*args, **kwargs)
            except Exception as e:
                response = e

            msg_out = self.codec.encode(response)
            self.transport.send(msg_out)
