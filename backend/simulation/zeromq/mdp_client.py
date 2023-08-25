import time

import orjson
import zmq
from loguru import logger

import MDP
from zhelpers import dump

"""Majordomo Protocol Client API, Python version.

Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.

Author: Min RK <benjaminrk@gmail.com>
Based on Java example by Arkadiusz Orzechowski
"""


class MajorDomoClient(object):
    """Majordomo Protocol Client API, Python version.

      Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
    """
    broker = None
    ctx = None
    client = None
    poller = None
    timeout = 2500
    retries = 3
    verbose = False

    def __init__(self, broker, verbose=False):
        self.broker = broker
        self.verbose = verbose
        self.ctx = zmq.Context()
        self.poller = zmq.Poller()
        self.logger = logger
        self.reconnect_to_broker()

    def reconnect_to_broker(self):
        """Connect or reconnect to broker"""
        if self.client:
            self.poller.unregister(self.client)
            self.client.close()
        self.client = self.ctx.socket(zmq.REQ)
        self.client.linger = 0
        self.client.connect(self.broker)
        self.poller.register(self.client, zmq.POLLIN)
        if self.verbose:
            self.logger.info("I: connecting to broker at %s..." % self.broker)

    def send(self, service, request):
        """Send request to broker and get reply by hook or crook.

        Takes ownership of request message and destroys it when sent.
        Returns the reply message or None if there was no reply.
        """
        if not isinstance(request, list):
            request = [request]
        request = [MDP.C_CLIENT, service] + request
        if self.verbose:
            self.logger.warning("I: send request to '%s' service: " % service)
            dump(request)
        reply = None

        retries = self.retries
        while retries > 0:
            self.client.send_multipart(request)
            try:
                items = self.poller.poll(self.timeout)
            except KeyboardInterrupt:
                break  # interrupted

            if items:
                msg = self.client.recv_multipart()
                if self.verbose:
                    self.logger.info("I: received reply:")
                    dump(msg)

                # Don't try to handle errors, just assert noisily
                assert len(msg) >= 3

                header = msg.pop(0)
                assert MDP.C_CLIENT == header

                reply_service = msg.pop(0)
                assert service == reply_service

                reply = msg
                break
            else:
                if retries:
                    self.logger.warning("W: no reply, reconnecting...")
                    self.reconnect_to_broker()
                else:
                    self.logger.warning("W: permanent error, abandoning")
                    break
                retries -= 1

        return reply

    def destroy(self):
        self.ctx.destroy()


if __name__ == "__main__":
    def main():
        verbose = True
        client = MajorDomoClient("tcp://localhost:5556", verbose)
        requests = 100000
        for i in range(requests):
            request = {
                "message": "Hellooooooo",
            }
            # send_request = pickle.dumps(request)
            # request2 = {
            #     "message": "Bruhhhhhhhh",
            # }
            send_request = orjson.dumps(request)
            try:
                client.send(b"matching", send_request)
                # client.send(b"bruh", request2)
            except KeyboardInterrupt:
                print("send interrupted, aborting")
                return
            time.sleep(1)

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
