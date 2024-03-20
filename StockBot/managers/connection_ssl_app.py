import asyncio
import threading
import time
import warnings
import queue
from StockBot.managers.connection_abstract import ConnectionManager
import ssl
import json

_CLIENT = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
_CLIENT.verify_mode = ssl.CERT_REQUIRED
_CLIENT.load_default_certs()


class ConnectionSSLAPP(ConnectionManager):
    HOST_NAME: str
    CLIENT_READ: asyncio.StreamReader
    STREAM_READ: asyncio.StreamReader
    CLIENT_SEND: asyncio.StreamWriter
    STREAM_SEND: asyncio.StreamWriter
    stream_queue: queue.Queue
    client_queue: queue.Queue

    def __init__(self, client, stream, host_name):
        self.HOST_NAME = host_name
        self.stream_queue = queue.Queue()
        self.client_queue = queue.Queue()
        self.connect(client, stream)

    def connect(self, client, stream):
        client_thread = threading.Thread(target=self.thread_ssl_client_function, args=client)
        stream_thread = threading.Thread(target=self.thread_ssl_stream_function, args=stream)

        print("Starting client")
        client_thread.start()
        print("Starting stream")
        stream_thread.start()

    def thread_ssl_client_function(self, client: str, port: str) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.ssl_client(client, port))
        loop.close()

    def thread_ssl_stream_function(self, stream: str, port: str) -> None:
        time.sleep(0.2)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.ssl_stream(stream, port))
        loop.close()

    async def ssl_client(self, client: str, port: str):
        self.CLIENT_READ, self.CLIENT_SEND = await asyncio.open_connection(client, port, ssl=_CLIENT)
        while True:
            message = (await self.CLIENT_READ.read(65536)).decode(encoding='utf-8')
            msg_list = message.split('\n')
            for msg in msg_list:
                if len(msg) > 0:
                    try:
                        (response, size) = json.JSONDecoder().raw_decode(msg)
                        self.client_queue.put(response)
                    except Exception as e:
                        print(e)
                        print(msg)

    async def ssl_stream(self, stream: str, port: str):
        self.STREAM_READ, self.STREAM_SEND = await asyncio.open_connection(stream, port, ssl=_CLIENT)
        while True:
            message = (await self.STREAM_READ.read(4096)).decode(encoding='utf-8')
            self.stream_queue.put(message)

    def send_client(self, message: str) -> bool:
        try:
            message = json.dumps(message)
            message = message.encode('utf-8')
            self.CLIENT_SEND.write(message)
            print("Client send")
            return True
        except Exception as e:
            warnings.warn(str(e))
            return False

    async def read_client(self, message):
        pass

    def send_stream(self, message):
        command = message["command"]
        try:
            message = json.dumps(message)
            message = message.encode('utf-8')
            self.STREAM_SEND.write(message)
            print("Subscribed to: " + command)
        except Exception as e:
            warnings.warn(str(e))

    async def read_stream(self, message):
        pass

    def handle_error(self, *args):
        pass
