
class Transport:
    ''' Interface class, used to pass function calls to another
        object. The concerete class will impliment this interface
        with a given transport protocol. E.g. Http requests.
    '''
    def send(self, msg):
        raise NotImplementedError

    def recieve(self, msg):
        raise NotImplementedError


class QueueTransport(Transport):
    def __init__(self, queue):
        self.queue = queue

    def send(self, msg):
        self.queue.put(msg)

    def recieve(self):
        return self.queue.get()
