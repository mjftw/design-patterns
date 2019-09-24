import asyncio
from aiohttp import web, ClientSession
from queue import Queue

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
    def __init__(self, rx_queue, tx_queue):
        self.rx_queue = rx_queue
        self.tx_queue = tx_queue

    def send(self, msg):
        self.tx_queue.put(msg)

    def recieve(self):
        return self.rx_queue.get()


class HttpTransport(Transport):
    def __init__(self, own_host=None, own_endpoint=None, own_port=None,
            dest_host=None, dest_endpoint=None, dest_port=None):
        self.own_host = own_host or '0.0.0.0'
        self.own_endpoint = own_endpoint or '/'
        self.own_port = own_port or 8080
        self.dest_host = dest_host or '0.0.0.0'
        self.dest_endpoint = dest_endpoint or '/'
        self.dest_port = dest_port or 8080

        self.rx_queue = Queue()

        self.app = web.Application()
        self.app.add_routes([web.post(self.own_endpoint, self._msg_recieve)])

        web.run_app(self.app, host=self.own_host, port=self.own_port)

    async def _msg_recieve(self, request):
        self.rx_queue.put(request.text)
        return web.Response(status=200)

    async def _msg_send(self, session, url, msg):
        async with session.post(url, text=msg) as response:
            return await response.status()

    async def _run_client(self, msg):
        async with ClientSession() as session:
            status = await self._msg_send(session, self.dest_host, msg)
            print(status)

    def send(self, msg):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run_client(msg))

    def recieve(self):
        return self.rx_queue.get()