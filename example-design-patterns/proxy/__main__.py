'''Example usage of Remote Proxy design pattern'''

from threading import Thread
from queue import Queue

from .proxy import ProxyClient, ProxyService
from .transport import QueueTransport


class Foo:
    ''' Example class to spoof '''

    def __init__(self):
        self.attr1 = 1
        self.attr2 = 2

    def difference(self, x, y):
        return abs(x - y)


def client_main(client_queue, service_queue, spoof_class):
    '''Run the proxy client'''
    transport = QueueTransport(client_queue, service_queue)
    spoof_proxy = ProxyClient(spoof_class, transport)

    attr1 = spoof_proxy.attr1
    print(attr1)

    spoof_proxy.attr1 = 10

    attr1 = spoof_proxy.attr1
    print(attr1)

    ans = spoof_proxy.difference(2, 7)
    print(ans)

    try:
        attr = spoof_proxy.not_an_attr
    except Exception as e:
        print(f'Caught exception: {type(e)}: {str(e)}')


def service_main(client_queue, service_queue, spoof_class):
    '''Run the proxy service'''
    spoof = spoof_class()

    transport = QueueTransport(service_queue, client_queue)
    proxy = ProxyService(spoof, transport)

    proxy.run()


def main():
    '''Setup the service and run the client'''
    spoof_class = Foo

    client_queue = Queue()
    service_queue = Queue()

    service_thread = Thread(target=service_main,
                            args=(client_queue, service_queue, spoof_class,))
    service_thread.start()

    client_main(client_queue, service_queue, spoof_class)


if __name__ == '__main__':
    main()
