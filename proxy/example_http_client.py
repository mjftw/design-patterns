from proxy import ProxyClient
from codec import PickleCodec
from transport import HttpTransport


class Foo:
    ''' Example class to spoof '''
    def __init__(self):
        self.attr1 = 1
        self.attr2 = 2

    def difference(self, x, y):
        return abs(x - y)


def main():
    codec = PickleCodec()

    transport = HttpTransport(own_port=5000, dest_port=5001)
    foo_proxy = ProxyClient(codec, transport)

    attr1 = foo_proxy.attr1
    print(attr1)

    foo_proxy.attr1 = 10

    attr1 = foo_proxy.attr1
    print(attr1)

    ans = foo_proxy.difference(2, 7)
    print(ans)

    try:
        attr = foo_proxy.not_an_attr
    except Exception as e:
        print(f'Caught exception: {type(e)}: {str(e)}')


if __name__ == '__main__':
    main()
