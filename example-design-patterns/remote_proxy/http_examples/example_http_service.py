from ..proxy import ProxyService
from ..transport import HttpTransport


class Foo:
    ''' Example class to spoof '''

    def __init__(self):
        self.attr1 = 1
        self.attr2 = 2

    def difference(self, x, y):
        return abs(x - y)


def main():
    foo = Foo()

    transport = HttpTransport(own_port=5001, dest_port=5000)
    proxy = ProxyService(foo, transport)

    proxy.run()
