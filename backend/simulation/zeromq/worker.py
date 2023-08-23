from datetime import datetime

import zmq
import os
from .settings import *
from loguru import logger
class Worker:
    def __init__(self):

        filename = os.path.join(LOG_FOLDER,
                                "client_%s.log" % (datetime.now().strftime("%Y-%m-%d")))
        self.logger = logger
        self.logger.add(filename, format="{time} {level} {message}", level="INFO")

        self.type = None
        self.folder_path = ""
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        connection_string = f"tcp://{SERVER_HOST}:{SERVER_PORT}"
        self.logger.info(f"Connecting to {connection_string}")
        self.socket.connect(connection_string)
        logging.info("Connect successfully!!!")

    def receive(self):
        try:
            msg = self.socket.recv_pyobj(flags=zmq.NOBLOCK)
        except:
            raise zmq.Again()

        return msg

    def send(self, msg):
        print(f"Send message to client: {msg}")
        # self.socket.send_pyobj(msg)
