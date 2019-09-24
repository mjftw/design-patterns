from threading import Thread
from queue import Queue

from proxy import ProxyClient, ProxyService
from codec import PickleCodec
from transport import QueueTransport


class Foo:
    ''' Example class to spoof '''
    def __init__(self):
        self.attr1 = 1
        self.attr2 = 2

    def difference(self, x, y):
        return abs(x - y)


def client_main(client_queue, service_queue):
    codec = PickleCodec()
    transport = QueueTransport(client_queue, service_queue)
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


def service_main(client_queue, service_queue):
    foo = Foo()

    codec = PickleCodec()
    transport = QueueTransport(service_queue, client_queue)
    proxy = ProxyService(foo, codec, transport)

    proxy.run()


def main():
    client_queue = Queue()
    service_queue = Queue()

    service_thread = Thread(target=service_main,
        args=(client_queue, service_queue,))
    service_thread.start()

    client_main(client_queue, service_queue)


if __name__ == '__main__':
    main()