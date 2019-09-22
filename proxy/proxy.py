def Transport:
    ''' Interface class, used to pass function calls to another
        object. The concerete class will impliment this interface
        with a given transport protocol. E.g. Http requests. '''
    def __init__(self):
        raise NotImplementedError

    def send(self, fn, *args, **kwargs):
        raise NotImplementedError

    def recieve(self, msg):
        raise NotImplementedError


# Client object helper
class ProxyClient:
    ''' The ProxyClient spoofs another object, pretending to be it.
        Any calls made to the ProxyClient are handed to the
        Transport class and sent to the ProxyService '''
    def __init__(self, transport):
        assert isinstance(transport, Transport)
        self.transport = transport


# Service object helper
class ProxyService:
    ''' The ProxyService handles calls ftom the ProxyClient via
        the Transport class. It then makes these same calls to
        the real object that the ProxyClient is spoofing.
        The response is then passed back to the ProxyClient via
        the Transport and handed back to the calling object'''
    def __init__(self, transport):
        assert isinstance(transport, Transport)
        self.transport = transport