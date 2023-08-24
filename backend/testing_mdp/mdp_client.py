"""Majordomo Protocol Client API, Python version.

Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.

Author: Min RK <benjaminrk@gmail.com>
Based on Java example by Arkadiusz Orzechowski
"""
import pickle

from loguru import logger
import sys

import zmq

import MDP
from zhelpers import dump

class MajorDomoClient(object):
    """Majordomo Protocol Client API, Python version.

      Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
    """
    broker = None
    ctx = None
    client = None
    poller = None
    timeout = 2500
    verbose = False

    def __init__(self, broker, verbose=False):
        self.broker = broker
        self.verbose = verbose
        self.ctx = zmq.Context()
        self.poller = zmq.Poller()
        # logging.basicConfig(format="%(asctime)s %(message)s",
        #                     datefmt="%Y-%m-%d %H:%M:%S",
        #                     level=logging.INFO)
        self.logger = logger
        self.logger.add("logs/mdp_client.log", rotation="500 MB", compression="zip", level="INFO")
        self.reconnect_to_broker()


    def reconnect_to_broker(self):
        """Connect or reconnect to broker"""
        if self.client:
            self.poller.unregister(self.client)
            self.client.close()
        self.client = self.ctx.socket(zmq.DEALER)
        self.client.linger = 0
        self.client.connect(self.broker)
        self.poller.register(self.client, zmq.POLLIN)
        if self.verbose:
            self.logger.info("I: connecting to broker at %s...", self.broker)

    def send(self, service, request):
        """Send request to broker
        """
        if not isinstance(request, dict):
            request = {"message": request}

        # Prefix request with protocol frames
        # Frame 0: empty (REQ emulation)
        # Frame 1: "MDPCxy" (six bytes, MDP/Client x.y)
        # Frame 2: Service name (printable string)
        protocol_frames = [b'', MDP.C_CLIENT, service]
        serialized_request = pickle.dumps(request)

        request_frames = protocol_frames + [serialized_request]
        if self.verbose:
            self.logger.warning("I: send request to '%s' service: ", service)
            dump(request_frames)
        self.client.send_multipart(request_frames)

    def recv(self):
        """Returns the reply message or None if there was no reply."""
        try:
            items = self.poller.poll(self.timeout)
        except KeyboardInterrupt:
            return # interrupted

        if items:
            # if we got a reply, process it
            msg = self.client.recv_multipart()
            if self.verbose:
                self.logger.info("I: received reply:")
                dump(msg)

            # Don't try to handle errors, just assert noisily
            assert len(msg) >= 4

            empty = msg.pop(0)
            header = msg.pop(0)
            assert MDP.C_CLIENT == header

            service = msg.pop(0)
            return msg
        else:
            self.logger.warning("W: permanent error, abandoning request")

if __name__ == "__main__":
    def main():
        verbose = True
        client = MajorDomoClient("tcp://localhost:5555", verbose)
        requests = 100000
        for i in range(requests):
            request = {
                "message": "Hellooooooo",
            }
            request2 = {
                "message": "Bruhhhhhhhh",
            }
            try:
                client.send(b"echo", request)
                client.send(b"bruh", request2)
            except KeyboardInterrupt:
                print("send interrupted, aborting")
                return

        count = 0
        while count < requests:
            try:
                reply = client.recv()
            except KeyboardInterrupt:
                break
            else:
                # also break on failure to reply:
                if reply is None:
                    break
            count += 1
        print("%i requests/replies processed" % count)
    main()