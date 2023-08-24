import zmq

from .settings import *
from datetime import datetime
from loguru import logger


class Client:
    def __init__(self):
        filename = os.path.join(LOG_FOLDER, "client_%s.log" % (datetime.now().strftime("%Y-%m-%d")))
        self.logger = logger
        self.logger.add(filename, format="{time} {level} {message}", level="INFO")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect(f"tcp://{CLIENT_HOST}:{CLIENT_PORT}")
        self.logger.info(f"Connected client to port {CLIENT_PORT}")
        self.socket.setsockopt(zmq.LINGER, 0)

    def send(self, msg):


        self.socket.send_pyobj(msg)
        # # Wait max 50 milliseconds for a reply, then complain
        # poller = zmq.Poller()
        # poller.register(self.socket, zmq.POLLIN)
        # poller.poll(50)
        self.logger.info(f"Send message to client: {msg}")

    # destructor
    def __del__(self):
        self.socket.close()
        self.context.term()
        self.logger.info("Close socket and context!!!")

    def close(self):
        self.socket.close()
        self.context.term()
        self.logger.info("Close socket and context!!!")


# if __name__ == "__main__":
#     client = Client()
#     client.send({'task_id': 15, 'folder_path': '/home/delus/Documents/Projects/SCO_DATA/swaptimizer_inputs_folder/26300b32-50b1-4346-ba4a-6a01117be2ce/swaptimizer_inputs'})
