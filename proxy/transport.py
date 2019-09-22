
class Transport:
    ''' Interface class, used to pass function calls to another
        object. The concerete class will impliment this interface
        with a given transport protocol. E.g. Http requests.
    '''
    def send(self, msg):
        raise NotImplementedError

    def recieve(self, msg):
        raise NotImplementedError


class QueueTransportClient(Transport):
    def __init__(self, client_queue, service_queue):
        self.client_queue = client_queue
        self.service_queue = service_queue

    def send(self, msg):
        self.service_queue.put(msg)

    def recieve(self):
        return self.client_queue.get()


class QueueTransportSerice(Transport):
    def __init__(self, client_queue, service_queue):
        self.client_queue = client_queue
        self.service_queue = service_queue

    def send(self, msg):
        self.client_queue.put(msg)

    def recieve(self):
        return self.service_queue.get()
