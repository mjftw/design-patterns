import asyncio
from threading import Thread
from aiohttp import web, ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from queue import Queue
import time


class TransportError(Exception):
    pass


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

        self.server_thread = Thread(
            target=self._run_server, args=(self._aiohttp_server(),))

        self.server_thread.start()

    # ======= Server =======
    def _aiohttp_server(self):
        app = web.Application()
        app.add_routes([web.post(self.own_endpoint, self._msg_recieve)])
        runner = web.AppRunner(app)
        return runner

    def _run_server(self, runner):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, self.own_host, self.own_port)
        loop.run_until_complete(site.start())

        print(f'Running server on {self.own_host}:{self.own_port}')
        loop.run_forever()

    async def _msg_recieve(self, request):
        msg = await request.read()
        self.rx_queue.put(msg)
        return web.Response(status=200)

    # ======= Client =======
    async def _msg_send(self, session, url, msg):
        delay = 0.05
        waited = 0
        max_delay = 10
        # Retry request with exponential backoff
        while True:
            try:
                async with session.post(url, data=msg) as response:
                    return response.status
            except ClientConnectorError as e:
                delay = delay * 2

                if delay >= max_delay:
                    delay = max_delay
                    raise TransportError(f'{str(e)}. No response after {waited}s')

                time.sleep(delay)
                waited += delay

    async def _run_client(self, msg):
        url = f'http://{self.dest_host}:{self.dest_port}{self.dest_endpoint}'
        status = None
        async with ClientSession() as session:
            status = await self._msg_send(session, url, msg)
        if status != 200:
            raise TransportError(f'Bad response from {url}: {status}')

    # ======= API =======
    def send(self, msg):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run_client(msg))

    def recieve(self):
        return self.rx_queue.get()
