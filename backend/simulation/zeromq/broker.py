import zmq
import os
from datetime import datetime
from settings import *
from loguru import logger

class Broker:
    def __init__(self):
        # Configure logging

        filename = os.path.join(LOG_FOLDER,
                                "broker_%s.log" % (datetime.now().strftime("%Y-%m-%d")))
        self.logger = logger
        self.logger.add(filename, format="{time} {level} {message}", level="INFO")

        self.context = zmq.Context()

        # Socket facing clients
        self.client = self.context.socket(zmq.PULL)
        self.client.bind(f"tcp://*:{CLIENT_PORT}")

        # Socket facing services
        self.sim = self.context.socket(zmq.PUSH)
        self.sim.bind(f"tcp://*:{SERVER_PORT}")
        self.logger.info(f"Connection from client at {CLIENT_PORT} to worker at {SERVER_PORT}")

    def connect(self):
        self.logger.info("Device ready. Press \'Ctrl+C\' to terminate.")

        zmq.device(zmq.QUEUE, self.client, self.sim)

    def __del__(self):
        self.client.close()
        self.sim.close()
        self.context.term()
        self.logger.info("Close socket and context!!!")


if __name__ == "__main__":
    broker = Broker()
    try:
        broker.connect()
        broker.logger.info("Starting...")
        broker.logger.info(f"tcp://*:{CLIENT_PORT}")
        broker.logger.info(f"tcp://*:{SERVER_PORT}")
        broker.logger.info('Broker device ready. Press \'Ctrl+C\' to terminate.')
    except KeyboardInterrupt:
        broker.logger.info("Terminated!!!")
    except Exception as e:
        print("Exception: ", e)
        broker.logger.exception("Broker device error: %s" % str(e))
    finally:
        del broker
