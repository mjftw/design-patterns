import inspect
import pickle

from transport import Transport, TransportError


class ProxyError(Exception):
    pass


# Client object helper
class ProxyClient:
    ''' The ProxyClient spoofs another object, pretending to be it.
        Any calls made to the ProxyClient are serialised using
        pickle and then handed to a Transport class and sent
        to the ProxyService. '''
    def __init__(self, target_class, transport):
        assert isinstance(transport, Transport)
        object.__setattr__(self, '_transport', transport)

        proxy_call = object.__getattribute__(self, 'proxy_call')
        try:
            real_target_class = proxy_call('__getattribute__', '__class__')
        except ProxyError as e:
            raise ProxyError(f'{str(e)}. Targeted class not in scope; different class to expected: {target_class}')
        if target_class != real_target_class:
            raise ProxyError('Targeted class is actually {} not {} as expected'.format(
                real_target_class, target_class))

    def proxy_call(self, fn_name, *args, **kwargs):
        transport = object.__getattribute__(self, '_transport')

        msg_out = pickle.dumps((fn_name, args, kwargs))
        transport.send(msg_out)
        msg_in = transport.recieve()
        try:
            response = pickle.loads(msg_in)
        except Exception as e:
            raise ProxyError(f'Message decode error: {str(e)}')

        if isinstance(response, Exception):
            raise response

        if not callable(response) or inspect.isclass(response):
            return response

        fn_name = args[0]

        def wrap(*fn_args, **fn_kwargs):
            msg_out = pickle.dumps((fn_name, fn_args, fn_kwargs))
            transport.send(msg_out)
            msg_in = transport.recieve()
            response = pickle.loads(msg_in)

            return response
        wrap.__name__ = fn_name

        return wrap

    #
    # proxying (special cases)
    #
    def __getattribute__(self, *args, **kwargs):
        proxy_call = object.__getattribute__(self, 'proxy_call')
        return proxy_call('__getattribute__', *args, **kwargs)

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
    ''' The ProxyService handles calls from the ProxyClient via
        the Transport class. It then makes these same calls to
        the real object that the ProxyClient is spoofing.
        The response is then passed back to the ProxyClient via
        the Transport and handed back to the calling object'''
    def __init__(self, service, transport):
        assert isinstance(transport, Transport)
        self.service = service
        self.transport = transport

    def run(self):
        while True:
            args = ()
            kwargs = {}
            fn_name = None
            response = None

            msg_in = self.transport.recieve()
            try:
                decoded = pickle.loads(msg_in),
                decoded = decoded[0]
            except Exception as e:
                response = TransportError(f'Message decode error: {str(e)}')

            if not response:
                if len(decoded) >= 1:
                    fn_name = decoded[0]
                if len(decoded) >= 2:
                    args = decoded[1]
                if len(decoded) >= 3:
                    kwargs = decoded[2]

                response = self.make_call(fn_name, *args, **kwargs)

            msg_out = pickle.dumps(response)
            self.transport.send(msg_out)

    def make_call(self, fn_name, *args, **kwargs):
        try:
            if not fn_name:
                response = TransportError('Invalid message format')
            elif fn_name == '__getattr__':
                self.print_fn_call('getattr', self.service, *args, **kwargs)
                response = getattr(self.service, *args, **kwargs)
            elif fn_name == '__delattr__':
                self.print_fn_call('delattr', self.service, *args, **kwargs)
                response = delattr(self.service, *args, **kwargs)
            elif fn_name == '__setattr__':
                self.print_fn_call('setattr', self.service, *args, **kwargs)
                response = setattr(self.service, *args, **kwargs)
            elif fn_name == '__nonzero__':
                self.print_fn_call('bool', self.service, *args, **kwargs)
                response = bool(self.service, *args, **kwargs)
            elif fn_name == '__str__':
                self.print_fn_call('str', self.service, *args, **kwargs)
                response = str(self.service, *args, **kwargs)
            elif fn_name == '__repr__':
                self.print_fn_call('repr', self.service, *args, **kwargs)
                response = repr(self.service, *args, **kwargs)
            elif fn_name == '__hash__':
                self.print_fn_call('hash', self.service, *args, **kwargs)
                response = hash(self.service, *args, **kwargs)
            else:
                fn = object.__getattribute__(self.service, fn_name)
                self.print_fn_call(fn_name, *args, **kwargs)
                response = fn(*args, **kwargs)
        except Exception as e:
            response = e

        return response

    def print_fn_call(self, fn_name, *args, **kwargs):
        args_str = ', '.join(str(a) for a in args)
        kwargs_str = ', '.join([f'{k}={v}' for k, v in kwargs.items()])
        fn_call = '{}({}{})'.format(
            fn_name,
            args_str,
            f', {kwargs_str}' if kwargs_str else ''
        )
        print(fn_call)
