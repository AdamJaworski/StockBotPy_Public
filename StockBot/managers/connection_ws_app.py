import json
import ssl
import time
import queue

from StockBot.managers.connection_abstract import ConnectionManager
import websocket as ws
import threading


class ConnectionWSAPP(ConnectionManager):
    STREAM: ws.WebSocketApp
    CLIENT: ws.WebSocketApp
    HOST_NAME:  str
    CLIENT_URL: str
    STREAM_URL: str
    stream_queue: queue.Queue
    client_queue: queue.Queue

    def __init__(self, client: str, stream: str, host_name):
        ws.enableTrace(True)
        self.stream_queue = queue.Queue()
        self.client_queue = queue.Queue()

        self.CLIENT_URL = client
        self.STREAM_URL = stream
        self.HOST_NAME  = host_name
        self.connect(client, stream)

    def connect(self, client, stream):
        self.CLIENT = ws.WebSocketApp(client,
                                      on_error=self.handle_error,
                                      on_message=self.read_client,
                                      on_close=self.on_close,
                                      on_open=self.on_open)
        self.STREAM = ws.WebSocketApp(stream,
                                      on_error=self.handle_error,
                                      on_message=self.read_stream,
                                      on_close=self.on_close)
        client_thread = threading.Thread(target=self.CLIENT.run_forever, args=[None, {"check_hostname": False, "cert_reqs": ssl.CERT_REQUIRED}])

        print("Starting client")
        client_thread.start()

    def on_open(self, *args):
        time.sleep(1.5)
        stream_thread = threading.Thread(target=self.STREAM.run_forever,
                                         args=[None, {"check_hostname": False, "cert_reqs": ssl.CERT_REQUIRED}])
        print("Starting stream")
        stream_thread.start()
        time.sleep(0.7)

    def on_close(self, *args):
        for arg in args:
            print(arg)

    def disconnect(self):
        self.CLIENT.close()
        self.STREAM.close()
        pass

    def send_client(self, message: str) -> bool:
        print("trying to send client")
        try:
            message = json.dumps(message)
            self.CLIENT.send(message)
            print("Client send")
            return True
        except Exception as e:
            ws.error(str(e))
            return False

    def read_client(self, *args):
        msg_list = args[1].split('\n')
        for msg in msg_list:
            if len(msg) > 0:
                (response, size) = json.JSONDecoder().raw_decode(msg)
                self.client_queue.put(response)

    def send_stream(self, message):
        try:
            message = json.dumps(message)
            self.STREAM.send(message)
        except Exception as e:
            ws.error(str(e))

    def read_stream(self, *args):
        self.stream_queue.put(args[1])

    def handle_error(self, *args):
        ws.debug("[!!!]Trying to handle error!")
        for error in args:
            ws.debug(str(error))
