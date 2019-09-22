from threading import Thread
from queue import Queue

from proxy import ProxyClient, ProxyService
from codec import PickleCodec
from transport import QueueTransport


class Foo:
    def __init__(self):
        self.attr1 = 1
        self.attr2 = 2

    def difference(self, x, y):
        return abs(x - y)


def client_main(queue):
    codec = PickleCodec()
    transport = QueueTransport(queue)
    foo_proxy = ProxyClient(codec, transport)

    attr1 = foo_proxy.attr1
    print(attr1)

    foo_proxy.attr1 = 10

    attr1 = foo_proxy.attr1
    print(attr1)

    ans = foo_proxy.difference(2, 7)
    print(ans)


def service_main(queue):
    foo = Foo()

    codec = PickleCodec()
    transport = QueueTransport(queue)
    proxy = ProxyService(foo, codec, transport)

    proxy.run()


def main():
    queue = Queue()

    service_thread = Thread(target=service_main, args=(queue,))
    service_thread.start()

    client_main(queue)


if __name__ == '__main__':
    main()