import json
import queue


class ConnectionManager:
    HOST_NAME:  str
    STREAM:     object
    CLIENT:     object
    stream_message: json
    client_message: json
    stream_queue: queue.Queue
    client_queue: queue.Queue
    # def __init__(self, client, stream, host_name):
    #     raise NotImplementedError

    def connect(self, client, stream):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def send_client(self, message: str) -> bool:
        raise NotImplementedError

    def read_client(self, message):
        raise NotImplementedError

    async def send_stream(self, message):
        raise NotImplementedError

    async def read_stream(self, message):
        raise NotImplementedError

    async def handle_error(self, *args):
        raise NotImplementedError
